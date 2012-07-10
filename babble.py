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
import logging

from modules import loadModules, checkModuleCommand, filterModule, pollModules

import irc
import tools


log = logging.getLogger('babble')


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
        checkModuleCommand(irc, cmd, body, sender, channel, private)
    else:
        filterModule(irc, body, channel, sender, msg)

_defaults = { 'logpath':    '.',
              'modules':    './modules',
              'debug':      False,
              'background': False,
            }

def main(config=None):
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

    log.info('Starting')

    loadModules(config)

    ircBot = irc.rbot(config, cb=processMessage)
    ircBot.start()

    log.info('starting IRC')

    lastPoll = time.time()

    while ircBot.active:
        ircBot.process()

        # loop thru the modules that have registered
        # a poll handler every 60 seconds
        if time.time() - lastPoll > 60:
            pollModules(ircBot)
            lastPoll = time.time()


if __name__ == "__main__":
    main()
