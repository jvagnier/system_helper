# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import platform
import app.lib
import app.commands


if "Windows" == platform.system():
    from .windows_settings import *
else:
    from .unix_settings import *


LOG_LEVEL = "DEBUG"
LOG_DIRECTORY = "logs"

PARSER_COMMANDS = {}
PARSER_COMMANDS["projects"] = app.commands.projects

SETUP_PATH = os.path.dirname(os.path.abspath(__file__))
SETUP_URL = "https://bootstrap.pypa.io/get-pip.py"
SETUP_PACKAGES = (
    "dulwich",
    "Jinja2",
    "mysql-python"
)


SETUP_DIRNAME = os.path.dirname(os.path.abspath(SETUP_FILENAME))
