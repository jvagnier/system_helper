# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from jinja2 import Template
from dulwich.client import get_transport_and_path
from dulwich.index import build_index_from_tree
from dulwich.repo import Repo

from app.lib.utils import create_directory


commit_template = Template("""
Id: {{ commit.id }}
Date: {{ commit.date }}
Emetteur: {{ commit.committer }}
Message:

{{ commit.message }}

""")


def render_commit(commit):
    return commit_template.render(commit=get_commit_data(commit))


def get_client(source):
    client, _ = get_transport_and_path(source)
    return client


def get_commit_data(commit):
    commit_data = {}
    commit_data['id'] = commit.id
    commit_data['committer'] = commit.committer
    commit_data['date'] = get_date_from_timestamp(commit.commit_time)
    commit_data['message'] = commit.message
    return commit_data


def init(path="."):
    abspath = os.path.abspath(path)
    gitpath = abspath + "/.git"
    if os.path.isdir(gitpath):
        repo = Repo(abspath)
    else:
        if os.path.isdir(abspath):
            repo = Repo.init(abspath)
        else:
            repo = Repo.init(abspath, mkdir=True)

    return repo


def fetch(repo, source, branch="master"):
    client, path = get_transport_and_path(source)

    refs = client.fetch(source, repo)
    ref = b'refs/heads/%s' % branch.encode('ascii')
    hexsha = refs[ref]

    repo.refs[b'HEAD'] = hexsha
    repo.refs[ref] = hexsha
    return hexsha


def checkout(repo, branch="master"):
    ref = b'refs/heads/%s' % branch.encode('ascii')
    hexsha = repo.refs[ref]
    build_index_from_tree(repo.path,
                          repo.index_path(),
                          repo.object_store,
                          repo[ref].tree)

    repo.refs[b'HEAD'] = hexsha
    return hexsha


def stage(repo, **files):
    repo.stage([str(f).encode('ascii') for f in files])


def commit(repo, *args, **kwargs):
    return repo.do_commit(*args, **kwargs)


def clone(repo, source, branch="master"):
    fetch(repo, source, branch)
    return checkout(repo, branch)



def main():
    print(os.getcwd())
    repo = init("/tmp/vcs")
    print(repo.path)
    source = "https://github.com/jvagnier/empty.git"
    clone(repo, source, "supernova")



if __name__ == '__main__':
    main()
