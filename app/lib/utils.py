# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import datetime

datetime_format = '%A, %d. %B %Y %H:%I:%S %z'

def get_date_from_timestamp(timestamp, format=datetime_format):
    d = datetime.datetime.fromtimestamp(int(timestamp))
    return d.strftime(format)


remove_directory_message = """
Le répertoire de destination existe: '%s'
Supprimer ? [o/N]
> """


def prompt_to_remove_directory(directory):
    message = remove_directory_message % directory
    recv = raw_input(message.encode('ascii'))

    if recv in ("o", "O"):
        return True
    else:
        return False


def create_directory(directory, force=False, prompt=True):
    if os.path.isdir(directory):
        if force is True:
            delete_required = True
        elif prompt is True:
            delete_required = prompt_to_remove_directory(directory)
        else:
            delete_required = False

        if delete_required is True:
            shutil.rmtree(directory)
            print("[x] Suppresion du répertoire '%s'" % directory)
        else:
            print("Abandon...")
            return False

    os.mkdir(directory)
    return True