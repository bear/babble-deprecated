#!/usr/bin/env python

"""
:copyright: (c) 2012 by Mike Taylor.
:license: BSD, see LICENSE for more details.
"""

import time
import logging

from ircbot import SingleServerIRCBot
from irclib import nm_to_n


log = logging.getLogger('babble')



class rbot(SingleServerIRCBot):
    def __init__(self, config, trigger='!', cb=None):
        self.config       = config
        self.active       = False
        self.joined       = False
        self.registerNick = False
        self.callback     = cb
        self.starttime    = time.strftime('%H:%M on %A, %d %B', time.gmtime(time.time()) )

        self.nickname = config.nickname
        self.password = config.password
        self.chanlist = config.channels
        self.server   = config.server
        self.realname = self.nickname
        self.port     = 6667
        self.trigger  = '!'

        if config.port is not None:
            self.port = config.port

        if config.trigger is not None:
            self.trigger = config.trigger

        if self.nickname is not None:
            self.nicklength = len(self.nickname)
            SingleServerIRCBot.__init__(self, [(self.server, self.port)], self.nickname, self.realname)
        else:
            raise Exception('nickname not defined, rbot init has stopped')

    def start(self):
        self._connect()
        self.active = True

    def stop(self):
        self.active = False
        self.ircobj.disconnect_all()

    def process(self):
        self.ircobj.process_once(0.1)

    def tell(self, target, message):
        self.connection.privmsg(target, message)

    def do_join(self, event, cmd, data):
        SingleServerIRCBot._on_join(self, self.connection, event)
        self.connection.join(data[1], data[2])

    def do_part(self, event, cmd, data):
        log.debug('do_part: %s %s %s %s' % (event, cmd, data[1], data[2]))

    def on_ctcp(self, serverconnection, event):
        if event.arguments()[0] == 'ACTION':
            event.arguments().pop(0)
            self.on_action(serverconnection, event)
        elif event.arguments()[0] == 'VERSION':
            serverconnection.ctcp_reply(nm_to_n(event.source()), self.config.version)
        elif event.arguments()[0] == 'PING':
            if len(event.arguments()) > 1:
                serverconnection.ctcp_reply(nm_to_n(event.source()), 'PING ' + event.arguments()[1])

    def on_action(self, serverconnection, event):
        log.debug('on_action: %s %s %s' % (nm_to_n(event.source()), str(event.arguments()), event.eventtype()))

    def on_privmsg(self, serverconnection, event):
        if self.callback is not None:
            sender  = nm_to_n(event.source())
            channel = event.target()
            self.callback(event.arguments()[0], sender, channel, True, self)

    def on_pubmsg(self, serverconnection, event):
        if self.callback is not None:
            sender  = nm_to_n(event.source())
            channel = event.target()
            self.callback(event.arguments()[0], sender, channel, False, self)

    def on_welcome(self, serverconnection, event):
        if len(self.chanlist) == 0:
            log.error('on_welcome called but we do not have any channels configured -- stopping')
            self.stop()
        else:
            log.info('on_welcome: %s' % self.server)

            if self.registerNick:
                log.debug('registering with nickserv')
                self.registerNick = False
                self.tell('nickserv', 'identify %s' % self.password)
                time.sleep(0.5)

            for chan in self.chanlist:
                if '|' in chan:
                    chan, pw = chan.split('|')
                else:
                    pw = ""
                log.info('joining %s' % chan)
                serverconnection.join(chan, pw)

    def on_join(self, serverconnection, event):
        self.joined = True
        chan        = event.target().lower()

        if chan not in self.chanlist:
            self.chanlist.append(chan)

    def on_part(self, serverconnection, event):
        if event.target() in self.chanlist:
            self.chanlist.remove(event.target())

        self.joined = (len(self.chanlist) > 0)

    def on_quit(self, serverconnection, event):
        if nm_to_n(event.source()) == self.nickname:
            self.joined = False

    def on_list(self, serverconnection, event):
        if len(event.arguments()) > 2:
            ch = event.arguments()[0]
            n  = event.arguments()[1]
            self.stats[ch] = n

