# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from app.lib.log.handlers import *
import logging

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[name])

    make_console_stream_handler(logger)
    make_last_command_file_handler(logger)
    make_error_file_handler(logger)
    make_info_file_handler(logger)
    make_debug_file_handler(logger)

    return logger
