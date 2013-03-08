#!/usr/bin/env python

""" echo module

"""



from yapsy.IPlugin import IPlugin

class echo(IPlugin):
    def activate(self):
        super(echo, self).activate()
        print "I've been activated!"

    def deactivate(self):
        super(echo, self).deactivate()
        print "I've been deactivated!"



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