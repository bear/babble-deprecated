#!/usr/bin/env python

""" http HEAD module

take the URL given, make an HTTP HEAD request and
return the information
"""

import logging

log = logging.getLogger('babble')

try:
    import requests
    active = True
except:
    log.error('unable to import the requests python package, please install it and reload the bot')
    active = False

def head(irc, msg, sender, channel, private):
    if active:
        r = requests.head(msg)

        irc.tell(channel, 'HTTP HEAD request for [%s] returned a status code of %d and the following headers' % (msg, r.status_code))

        s = ''
        for header in r.headers:
            s += '%s = %s; ' % (header, r.headers[header])

        irc.tell(channel, s)

head.commands = ['head',]

