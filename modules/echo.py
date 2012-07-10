#!/usr/bin/env python

""" echo module

"""


def echo(irc, msg, sender, channel, private):
    irc.tell(channel, 'echo [%s]' % msg)

echo.commands = ['echo',]

def foo(irc, msg, sender, channel, private):
    irc.tell(channel, 'bar')

foo.commands = ['foo',]
