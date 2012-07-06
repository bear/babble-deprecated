#!/usr/bin/env python

"""
:copyright: (c) 2012 by Mike Taylor.
:license: BSD, see LICENSE for more details.
"""

import os
import imp

from multiprocessing import Process, Queue, get_logger
from Queue import Empty


log         = get_logger()
ircModules  = {}
ircCommands = {}
ircFilters  = []


def loadModules(config, qIRC):
    log.info('looking for modules to load')
    filenames = []

    for filename in os.listdir(config.modules):
        if filename.endswith('.py') and not filename.startswith('_'):
            filenames.append(os.path.join(config.modules, filename))

    for filename in filenames:
        fname = os.path.basename(filename)[:-3]

        q = Queue()
        p = Process(target=handleModule, name=fname, args=(fname, filename, q, qIRC, config))
        ircModules[fname] = { 'process': p,
                              'queue':   q,
                            }
        p.start()

def handleModule(moduleName, filename, qMsg, qIRC, config):
    log.info('initializing module %s [%s]' % (moduleName, filename))
    commands = {}
    filters  = []

    try:
        module = imp.load_source(moduleName, filename)

        if hasattr(module, 'setup'):
            log.info('calling setup for %s' % moduleName)
            module.setup(config)

        for item, obj in vars(module).iteritems():
            if hasattr(obj, 'commands'):
                for cmd in obj.commands:
                    log.info('registering command %s' % cmd)
                    qIRC.put(('command', moduleName, cmd))
                    commands[cmd] = obj
            if hasattr(obj, 'filters'):
                for cmd in obj.filters:
                    log.info('registering filter %s' % cmd)
                    qIRC.put(('filter', moduleName))
                    filters.append(obj)

    except:
        module = None
        log.error('Unable to load module %s' % moduleName, exc_info=True)
        qIRC.put(('module', 'remove', moduleName))

    if module is not None:
        while True:
            try:
                item = qMsg.get(False)
            except Empty:
                item = None

            if item is not None:
                cmd, msg, sender, channel, private = item
                log.info('processing %s' % cmd)
                if cmd == 'filter':
                    for func in filters:
                        func(msg, sender, channel, private, qIRC)
                else:
                    commands[cmd](msg, sender, channel, private, qIRC)

def checkModuleCommand(cmd, body, sender, channel, private):
    if cmd in ircCommands:
        mod = ircCommands[cmd]
        log.info('send msg to module %s for command %s' % (mod, cmd))
        ircModules[mod]['queue'].put((cmd, body), sender, channel, private)

def filterModule(body, sender, channel, private):
    for mod in ircFilters:
        log.info('send msg to module %s for filter' % mod)
        ircModules[mod]['queue'].put(('filter', body, sender, channel, private))

def registerCommand(cmd, module):
    log.info('registering %s %s' % (cmd, module))
    ircCommands[cmd] = module

def registerFilter(module):
    log.info('registering filter %s' % module)
    ircFilters.append(module)
