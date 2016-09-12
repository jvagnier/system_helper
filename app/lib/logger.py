# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging

from settings import LOG_LEVEL, LOG_DIRECTORY


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


formatter = logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s")


handler_console = logging.StreamHandler(stream=sys.stdout)
handler_out = logging.FileHandler("logs/out.log", mode="w", encoding="utf-8")
handler_debug = logging.FileHandler("logs/debug.log", mode="a", encoding="utf-8")
handler_info = logging.FileHandler("logs/info.log", mode="a", encoding="utf-8")
handler_critical = logging.FileHandler("logs/error.log", mode="a", encoding="utf-8")


handler_console.setFormatter(formatter)
handler_out.setFormatter(formatter)
handler_debug.setFormatter(formatter)
handler_info.setFormatter(formatter)
handler_critical.setFormatter(formatter)


handler_console.setLevel(logging.DEBUG)
handler_out.setLevel(logging.DEBUG)
handler_debug.setLevel(logging.DEBUG)
handler_info.setLevel(logging.INFO)
handler_critical.setLevel(logging.CRITICAL)


handler_console.addFilter(MaxLogLevel(logging.WARNING))
handler_out.addFilter(MinLogLevel(logging.DEBUG))
handler_debug.addFilter(MaxLogLevel(logging.DEBUG))


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logger = logging.getLogger(__file__)
logger.setLevel(LOG_LEVELS[LOG_LEVEL])

logger.addHandler(handler_out)
logger.addHandler(handler_console)
logger.addHandler(handler_debug)
logger.addHandler(handler_info)
logger.addHandler(handler_critical)
