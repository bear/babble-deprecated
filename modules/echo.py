#!/usr/bin/env python

""" echo module

"""


def echo(msg, sender, channel, private, irc):
    irc.put(('irc', channel, 'echo [%s]' % msg))

echo.commands = ['echo', "foo"]
