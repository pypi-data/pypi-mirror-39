# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from os import environ, access, X_OK

from gitcepter import VERSION

env_server = False


def get_exe_path(exe):
    for dir_path in environ['PATH'].split(':'):
        path = dir_path.strip('"') + '/' + exe
        if access(path, X_OK):
            return path


def iter_buffer(iterable, amount):
    assert amount > 1
    memo = []
    for elem in iterable:
        if elem is not None:
            memo.append(elem)
            if len(memo) < amount:
                continue
        yield memo.pop(0)

    for elem in memo:
        yield elem


def version():
    return '.'.join(str(v) for v in VERSION)


git_exe_path = get_exe_path('git')
jar_exe_path = get_exe_path('jar')
java_exe_path = get_exe_path('java')
