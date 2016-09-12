#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import argparse
import shutil
import datetime
import time
from jinja2 import Template
from dulwich.client import get_transport_and_path
from dulwich.index import build_index_from_tree
from dulwich.repo import Repo


remove_directory_prompt = b"""[x] Action requise:
  Le répertoire de destination existe: '%s'
> Supprimer ? [o/N] """


datetime_format = '%A, %d. %B %Y %H:%I:%S %z'


def get_date_from_timestamp(timestamp, format=datetime_format):
    d = datetime.datetime.fromtimestamp(int(timestamp))
    return d.strftime(format)


def get_commit_data(commit):
    commit_data = {}
    commit_data['id'] = commit.id
    commit_data['committer'] = commit.committer
    commit_data['date'] = get_date_from_timestamp(commit.commit_time)
    commit_data['message'] = commit.message
    return commit_data


commit_template = Template("""
Id: {{ commit.id }}
Date: {{ commit.date }}
Emetteur: {{ commit.committer }}
Message:

{{ commit.message }}

""")


def render_commit(commit):
    return commit_template.render(commit=get_commit_data(commit))


def clone_from(source, destination, branch="master", force=False):
    if os.path.isdir(destination):
        if force is False:
            prompt = remove_directory_prompt % destination.encode('ascii')
            recv = raw_input(prompt)

            if not recv in ("o", "O"):
                print("Abandon...")
                sys.exit(2)

        shutil.rmtree(destination)
        print("[x] Suppresion du répertoire '%s'" % destination)

    transport, path = get_transport_and_path(source)

    print("[x] Initialisation du nouveau répertoire '%s'" % destination)
    repo = Repo.init(destination, mkdir=True)

    print("[x] Vérification de la source '%s'" % source)
    remote_refs = transport.fetch(source, repo)
    remote_branch = b'refs/heads/%s' % branch.encode('ascii')

    print("[x] Récupération de la branche '%s'" % branch)
    hexsha = remote_refs[remote_branch]
    repo.refs[remote_branch] = hexsha
    build_index_from_tree(repo.path,
                          repo.index_path(),
                          repo.object_store,
                          repo[remote_branch].tree)

    last_commit = repo.get_object(hexsha)
    print("[x] Dernière révision:")
    print(render_commit(last_commit))

    print("[-] Répertoire local synchronisé avec '%s'" % source)
    return repo


COMMANDS = {
    "clone": clone_from
}


def make_parser():
    parser = argparse.ArgumentParser("scm")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("-b", dest="branch", default="master")
    parser.add_argument("-f", dest="force", action="store_true", default=False)
    return parser


PARSERS = [
    ("clone", get_clone_parser)
]


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser("scm")
    subparsers = parser.add_subparsers(dest="command")

    for name, parent in PARSERS:
        subparser = parent()
        subparsers.add_parser(name, parents=[subparser], add_help=False)

    args = parser.parse_args(argv)
    args = dict(vars(args))

    command = args.pop('command')
    callback = COMMANDS[command]
    callback(**args)


if __name__ == '__main__':
    main()
