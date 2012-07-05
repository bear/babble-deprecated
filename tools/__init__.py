#!/usr/bin/env python

"""
:copyright: (c) 2012 by Mike Taylor.
:license: BSD, see LICENSE for more details.
"""

import os
import json
import logging

from logging.handlers import RotatingFileHandler
from multiprocessing import get_logger


log = get_logger()


def relativeDelta(td):
    s = ''
    if td.days < 0:
        t = "%s ago"
    else:
        t = "in %s"

    days    = abs(td.days)
    seconds = abs(td.seconds)
    minutes = seconds / 60
    hours   = minutes / 60
    weeks   = days / 7
    months  = days / 30
    years   = days / 365

    if days == 0:
        if seconds < 20:
            s = 'just now'
        if seconds < 60:
            s = '%d seconds' % seconds
            s = t % s
        if seconds < 120:
            s = t % 'a minute'
        if seconds < 3600:
            s = '%d minutes' % minutes
            s = t % s
        if seconds < 7200:
            s = t % 'an hour'
        if seconds < 86400:
            s = '%d hours' % hours
            s = t % s
    else:
        if days == 1:
            if td.days < 0:
                s = 'yesterday'
            else:
                s = 'tomorrow'
        elif days < 7:
            s = '%d days' % days
            s = t % s
        elif days < 31:
            s = '%d weeks' % weeks
            s = t % s
        elif days < 365:
            s = '%d months' % months
            s = t % s
        else:
            s = '%d years' % years
            s = t % s

    return s

class Config(dict):
    def __init__(self, defaults=None):
        self.configFile = None
        if defaults is not None:
            self.defaults = defaults

    def load(self, filename, clear=False):
        if clear:
            self.clear()

        for key in self.defaults:
            self[key] = self.defaults[key]

        if os.path.isfile(filename):
            try:
                d = json.loads(' '.join(open(filename, 'r').readlines()))
                for key in d:
                    self[key] = d[key]

                self.configFile = filename
            except:
                log.warning('Error during loading of the configuration file [%s]' % filename, exc_info=True)

    def __getattr__(self, attributeName):
        if attributeName in self:
            return self[attributeName]
        else:
            return None

def initLogs(config):
    if config.logpath is not None:
        fileHandler   = RotatingFileHandler(os.path.join(config.logpath, '%s.log' % config.ourName), maxBytes=1000000, backupCount=99)
        fileFormatter = logging.Formatter('%(asctime)s %(levelname)-7s %(processName)s: %(message)s')

        fileHandler.setFormatter(fileFormatter)

        log.addHandler(fileHandler)
        log.fileHandler = fileHandler

    if not config.background:
        echoHandler   = logging.StreamHandler()
        echoFormatter = logging.Formatter('%(levelname)-7s %(processName)s: %(message)s')

        echoHandler.setFormatter(echoFormatter)

        log.addHandler(echoHandler)
        log.info('echoing')

    if config.debug:
        log.setLevel(logging.DEBUG)
        log.info('debug level is on')
    else:
        log.setLevel(logging.INFO)
