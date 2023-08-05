
# -*- coding: utf-8 -*-
import datetime
import os
import shutil

prefix_cache_dir = ".cache"


def file_extension(path):
    return os.path.splitext(path)[1]


def file_exists(path):
    return os.path.exists(path)


def file_to_text(path):
    f = open(path, "r", encoding='utf-8')
    return '\n'.join(f.readlines())


def mk_cache(dir_type):
    now_time = datetime.datetime.now()
    date_str = now_time.strftime("%Y%m%d%H%M%S%s")

    cache_dir = prefix_cache_dir + "/" + date_str + "/" + dir_type

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir


def rm_cache(dir_path=None):
    """ del cache directory """
    if not dir_path and os.path.exists(prefix_cache_dir):
        shutil.rmtree(prefix_cache_dir)
        return
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def save_file(output_dir, file):
    from gitcepter.changes import ChangedFile
    assert isinstance(file, ChangedFile)
    parent = output_dir + "/" + file.get_file_parent()
    if not os.path.exists(parent):
        os.makedirs(parent)
    path = output_dir + "/" + file.path
    fp = open(path, "wb")
    fp.write(file.get_content())
    fp.close()
