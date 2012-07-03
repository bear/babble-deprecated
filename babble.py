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


import os
import imp
import logging

from multiprocessing import Process, Queue, get_logger, log_to_stderr
from Queue import Empty


if __name__ == "__main__":
    print "currently I don't say much, go pester bear to add more code!"