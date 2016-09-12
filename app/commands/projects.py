#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import os
import argparse
from app.lib.vcs import clone, init


def make_command():
    projects_parser = argparse.ArgumentParser("projects")
    root_group = projects_parser.add_mutually_exclusive_group()
    root_group.add_argument("--clone", dest="clone", action="store_true", default=False)
    clone_group = root_group.add_mutually_exclusive_group()
    clone_group.add_argument("--source")
    clone_group.add_argument("--destination")
    clone_group.add_argument("-b", dest="branch", default="master")
    clone_group.add_argument("-f", dest="force", action="store_true", default=False)
    return projects_parser


def run(*args, **kwargs):
    if "clone" in kwargs and True is kwargs.pop("clone"):
        print(os.getcwd())
        repo = init("/tmp/vcs")
        print(repo.path)
        source = "https://github.com/jvagnier/empty.git"
        clone(repo, **kwargs)
