# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import clone

from argparse import ArgumentParser

prog = "projects"
parents = [clone]


def make_nested_options(prog, parser=None, parents=None):
    if parser is None:
        parser = ArgumentParser(prog)

    if parents is not None:
        subparsers  = parser.add_subparsers(dest=prog)
        for module in parents:
            subparser = subparsers.add_parser(module.prog)
            module.make_options(subparser)

    clone_parser = subparsers.add_parser('clone')
    clone.make_options(clone_parser)
    return parser


def guess_clone_params(kwargs):
    in_params = [kwargs.pop(p) for p in ("source", "branch")]
    if None in in_params:
        raise ValueError('invalid argument')
    return in_params


def run(*args, **kwargs):
    command_name = kwargs.pop('projects')
    if "clone" in kwargs and True is kwargs.pop("clone"):
        in_params = guess_clone_params(kwargs)
        repo = init("/tmp/vcs")
        clone(repo, *in_params)
    raise ValueError("arguments required")