#!/usr/bin/env python

"""
:copyright: (c) 2012 by Mike Taylor.
:license: BSD, see LICENSE for more details.
"""

# import os
# import imp
# import logging

# from yapsy.VersionedPluginManager import VersionedPluginManager
# from yapsy.PluginManager import PluginManagerSingleton

# log         = logging.getLogger('babble')
# ircModules  = {}
# ircCommands = {}
# ircFilters  = []
# ircPollers  = []


# PluginManagerSingleton.setBehaviour([
#     VersionedPluginManager,
# ])

# manager = PluginManagerSingleton.get()

# def loadModules(config):
#     log.info('loading modules')

#     manager.setPluginInfoExtension("plugin")
#     manager.setPluginPlaces(config.modules.path)

#     manager.collectPlugins()

#     for item in manager.getAllPlugins():
#         print info.name
#         print info.plugin_object
#         print info

    # for filename in filenames:
    #     log.info('loading module %s' % filename)
    #     moduleName = os.path.basename(filename)[:-3]

    #     try:
    #         module = imp.load_source(moduleName, filename)

    #         ircModules[moduleName] = module

    #         if hasattr(module, 'setup'):
    #             log.info('calling setup for %s' % moduleName)
    #             module.setup(config)

    #         for item, obj in vars(module).iteritems():
    #             if hasattr(obj, 'commands'):
    #                 for cmd in obj.commands:
    #                     log.info('registering command %s' % cmd)
    #                     ircCommands[cmd] = (obj, filename)
    #             if hasattr(obj, 'filters'):
    #                 log.info('registering filter %s' % cmd)
    #                 ircFilters.append((obj, filename))
    #             if hasattr(obj, 'timer'):
    #                 log.info('registering timer')
    #                 ircPollers.append((obj, filename))
    #     except:
    #         module = None
    #         log.error('Unable to load module %s' % filename, exc_info=True)


def checkModuleCommand(irc, cmd, body, sender, channel, private):
    if cmd in ircCommands:
        obj, mod = ircCommands[cmd]
        log.info('send msg to module %s for command %s' % (mod, cmd))
        obj(irc, body, sender, channel, private)

def filterModule(irc, body, sender, channel, private):
    for obj, mod in ircFilters:
        log.info('send msg to module %s for filter' % mod)
        obj(irc, body, sender, channel, private)

def pollModules(irc):
    for obj, mod in ircPollers:
        obj(irc)
