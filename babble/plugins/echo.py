#!/usr/bin/env python

""" echo module

"""
import time

from multiprocessing import Process, Queue
from Queue import Empty

from yapsy.IPlugin import IPlugin

class echo(IPlugin):
    def activate(self, events, qIrc):
        super(echo, self).activate()

        self.events = events
        self.irc    = qIrc
        self.p      = Process(target=self.handleEvents, args=(events, qIrc))

        self.p.start()

    def deactivate(self):
        super(echo, self).deactivate()

        self.events(('echo', 'shutdown'))

        self.p.join()

    def handleEvents(self, events, irc):
        while True:
            try:
                event = events.get(False)

                if event is not None:
                    if event[0] == 'irc':
                        print 'echo event handler', event
            except Empty:
                time.sleep(0.1)

# def echo(irc, msg, sender, channel, private):
#     irc.tell(channel, 'echo [%s]' % msg)

# echo.commands = ['echo',]

# def foo(irc, msg, sender, channel, private):
#     irc.tell(channel, 'bar')

# foo.commands = ['foo',]

# def test(irc, msg, sender, channel, private):
#     irc.tell(channel, msg.replace(' ', ''))

# test.filters = True

# def poll(irc):
#     pass

# poll.timer = True