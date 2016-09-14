# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import


class StrictLogLevel(object):
    def __init__(self, level):
        self._level = level

    def filter(self, log_record):
        return (log_record.levelno >= self._level)


class MinLogLevel(object):
    def __init__(self, level):
        self._level = level

    def filter(self, log_record):
        return (log_record.levelno >= self._level)


class MaxLogLevel(object):
    def __init__(self, level):
        self._level = level

    def filter(self, log_record):
        return (log_record.levelno <= self._level)
