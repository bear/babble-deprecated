#!/usr/bin/env python

"""
babble - another python bot

:copyright: (c) 2012 by Mike Taylor.
:license: BSD, see LICENSE for more details.

Requires:
    irc lib
"""

VERSION = (0, 1, 0, "alpha")

__author__       = 'Mike Taylor'
__contact__      = 'bear@code-bear.com'
__copyright__    = 'Copyright 2012, Mike Taylor'
__license__      = 'BSD'
__site__         = 'https://github.com/bear/babble'
__version__      = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__contributors__ = []


import os, sys
import time

from modules import loadModules, checkModuleCommand, filterModule, registerCommand, registerFilter

from multiprocessing import Queue, get_logger
from Queue import Empty

import irc
import tools


log      = get_logger()
ircQueue = Queue()


def processMessage(msg, sender, channel, private, irc):
    log.info(u'%s:%s %s' % (channel, sender, msg))

    args = msg.split(' ', 1)
    cmd  = None
    body = ''

    if args[0].startswith(irc.trigger):
        cmd = args[0][1:]
        body = ' '.join(args[1:])
    else:
        if (len(args) > 1) and (args[0] == irc.nickname):
            cmd  = args[1]
            body = ' '.join(args[2:])

    if cmd is not None:
        checkModuleCommand(cmd, body, sender, channel, private)
    else:
        filterModule(body, channel, sender, msg)

_defaults = { 'logpath':    '.',
              'modules':    './modules',
              'debug':      False,
              'background': False,
            }

def main(config=None):
    log.info('Starting')

    if config is None:
        config = tools.Config(_defaults)

        config.appPath = os.getcwd()
        config.ourName = os.path.splitext(os.path.basename(sys.argv[0]))[0]

        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            configFile = sys.argv[1]
        else:
            configFile = os.path.join(config.appPath, '%s.cfg' % config.ourName)

        if os.path.isfile(configFile):
            config.load(configFile)

    tools.initLogs(config)

    loadModules(config, ircQueue)

    ircBot = irc.rbot(config, cb=processMessage)
    ircBot.start()

    log.info('starting IRC')

    while ircBot.active:
        ircBot.process()

        try:
            msg = ircQueue.get(False)

            if msg is not None:
                if msg[0] == 'irc':
                    ircBot.tell(msg[1], msg[2])
                elif msg[0] == 'command':
                    registerCommand(msg[2], msg[1])
                elif msg[0] == 'filter':
                    registerFilter(msg[1])
        except Empty:
            time.sleep(0.1)


if __name__ == "__main__":
    main()