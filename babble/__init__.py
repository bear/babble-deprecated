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
__contact__      = 'bear@bear.im'
__copyright__    = 'Copyright 2012, Mike Taylor'
__license__      = 'BSD'
__site__         = 'https://github.com/bear/babble'
__version__      = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__contributors__ = []


import os, sys
import time
import atexit
import logging

from Queue import Empty
from multiprocessing import Process, Queue

from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton

import irc
from bearlib import bConfig, bLogs, daemonize


qEvents = Queue()
qIrc    = Queue()
log     = logging.getLogger()

def loadPlugins(config, qEvents, qIrc):
    log.info('loading plugins from [%s]' % config.path)
    # logging.getLogger('yapsy').setLevel(logging.DEBUG)

    PluginManagerSingleton.setBehaviour([
        VersionedPluginManager,
    ])
    manager = PluginManagerSingleton.get()

    manager.setPluginInfoExtension("plugin")
    manager.setPluginPlaces([os.path.abspath(config.path)])

    manager.collectPlugins()

    plugins = {}

    for item in manager.getAllPlugins():
        print item.name
        print item.plugin_object
        print item
        qPlugin = Queue()
        plugins[item.name.lower()] = (item, qPlugin)
        item.plugin_object.activate(qPlugin, qIrc)

    print "plugins loaded", qEvents

    while True:
        try:
            event = qEvents.get(False)

            if event is not None:
                target = event[0]

                if target == 'babble':
                    for plugin in plugins:
                        plugins[plugin][1].put(event)
                elif target == 'irc':
                    for plugin in plugins:
                        plugins[plugin][1].put(event)
                else:
                    if target in plugins:
                        plugins[target][1].put(event)
        except Empty:
            time.sleep(0.1)

    print "leaving loadPlgins"

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
        qEvents(('irc', (channel, sender, msg, body)))
        # filterModule(irc, body, channel, sender, msg)

def shutdown():
    qEvents.put(('babble', 'shutdown',))
    logging.shutdown()

def main():
    config = bConfig('babble')
    config.parseCommandLine()
    config.loadConfigFile()

    bLogs(config)

    log = logging.getLogger(config.ourname)

    atexit.register(shutdown)

    if config.daemon:
        daemonize(config)

    if hasattr(config, 'irc'):
        ircBot = irc.rbot(config.irc, cb=processMessage)
        ircBot.start()

        log.info('starting IRC')

        p = Process(target=loadPlugins, args=(config.plugins, qEvents, qIrc))
        p.start()

        lastPoll = time.time()

        while ircBot.active:
            ircBot.process()

            try:
                event = qIrc.get(False)

                if event is not None:
                    print 'irc send event', event

            except Empty:
                time.sleep(1)

            # loop thru the modules that have registered
            # a poll handler every 60 seconds
            if time.time() - lastPoll > 60:
                qEvents.put(('babble', 'ping'))
                lastPoll = time.time()

        p.join()
