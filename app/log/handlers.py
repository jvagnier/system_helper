# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from app.lib.log.filters import *
import sys
import logging

__all__ = [
    "make_info_file_handler",
    "make_error_file_handler",
    "make_last_command_file_handler",
    "make_debug_file_handler",
    "make_console_stream_handler"
]

formatter = logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s")


def make_console_stream_handler(logger):
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(MaxLogLevel(logging.WARNING))
    logger.addHandler(handler)


def make_last_command_file_handler(logger):
    handler = logging.FileHandler("logs/out.log", mode="w", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(MinLogLevel(logging.DEBUG))
    logger.addHandler(handler)


def make_debug_file_handler(logger):
    handler = logging.FileHandler("logs/debug.log", mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(MaxLogLevel(logging.DEBUG))
    logger.addHandler(handler)


def make_info_file_handler(logger):
    handler = logging.FileHandler("logs/info.log", mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


def make_error_file_handler(logger):
    handler = logging.FileHandler("logs/error.log", mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.CRITICAL)
    logger.addHandler(handler)
