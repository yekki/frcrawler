# -*- coding: utf-8 -*-

import os, shutil

STAGE_DIR = os.path.join(os.getcwd(), 'stage')


def cleanup_dirs(*dirs, rmdir=False):
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        if not rmdir:
            os.makedirs(dir)
