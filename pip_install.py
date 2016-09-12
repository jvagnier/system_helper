#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from settings import *
from logger import logger

import os
import subprocess as sp
import urllib
import shutil


class CommandResult(object):

    @property
    def code(self):
        return self.command.returncode

    @property
    def message(self):
        if self.command.returncode > 0:
            return self.command.stderr
        else:
            return self.command.stdout

    def __init__(self, command):
        self.command = command

    def __str__(self):
        return self.message

    def __repr__(self):
        return "CommandResult: returncode=%d, message=%s" % (
            self.code,
            self.message
        )


class Command(object):

    def __init__(self, string):
        if isinstance(string, (list, tuple)):
            string = " ".join(string)

        self.string = string
        self.stdout = None
        self.stderr = None
        self.returncode = None
        self.process = None

    def __str__(self):
        return self.string

    def __repr__(self):
        return "Command: string=%s" % self.string

    def run(self, catch_errors=False):
        logger.debug("Processus commande: %s" % self.string)
        process = sp.Popen(self.string,
                        stdin=sp.PIPE,
                        stdout=sp.PIPE,
                        stderr=sp.PIPE,
                        shell=True)

        logger.debug("Processus pid: %d" % process.pid)
        stdout, stderr = process.communicate()
        process.stdin.close()
        returncode = process.wait()

        logger.debug("Processus code de retour: %d" % returncode)
        if catch_errors is True and returncode > 0:
            logger.error("Sortie d'erreur:\n%s" % stdout)
            raise SystemExit(returncode)

        self.stdout = stdout.strip()
        self.stderr = stderr.strip()
        self.returncode = returncode
        self.process = process

        return CommandResult(self)


def download():
    if os.path.isdir(SETUP_DIRNAME):
        logger.warn("Suppression du répertoire %s" % SETUP_DIRNAME)
        shutil.rmtree(SETUP_DIRNAME)

    logger.info("Création du nouveau répertoire %s" % SETUP_DIRNAME)
    os.mkdir(SETUP_DIRNAME)

    logger.info("Téléchargement:\nSource: %s\nDestination: %s" % (SETUP_URL, SETUP_FILENAME))
    urllib.urlretrieve(SETUP_URL, SETUP_FILENAME)

    logger.warn("Changement des droits d'accès sur: %s (0755)" % SETUP_FILENAME)
    os.chmod(SETUP_FILENAME, 0755)


def install():
    result = Command(("python", SETUP_FILENAME, "--user")).run(True)


def requirements():
    install_pip = ("python", "-m", "pip", "install", "--user") + SETUP_PACKAGES
    save_req = ("python", "-m", "pip", "freeze", "--user", "|", "tee", REQ_FILENAME)

    install_pip_result = Command(install_pip).run(True)
    logger.info("Message de sortie:\n%s" % install_pip_result.message)
    save_req_result = Command(("python", SETUP_FILENAME, "--user")).run(True)



check_installed_message = """
Pip est déjà installé... Abandon!
Version : %s
Python  : %s
Site    : %s
""".strip()


def check_installed():
    command_result = Command("python -m pip -V").run(False)
    command_message = command_result.message
    if command_message.startswith("pip 8"):
        return True
    elif command_message.endswith("No module named pip"):
        return False
    else:
        return None


def main():
    installed = check_installed()
    if installed is True:
        logger.warn("Pip est déjà installé...")
    elif installed is False:
        download()
        install()
        requirements()
    else:
        logger.critical("Erreur inconnue")


if __name__ == '__main__':
    main()
