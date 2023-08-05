# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
from getopt import getopt
from sys import stdout
from traceback import print_exc

from gitcepter import consts, env
from gitcepter.checks import CommitMessageCheck, Checkstyle, JsonCheck, XmlCheck
from gitcepter.changes import LocalChanges, ChangedFile
from gitcepter.file import file_to_text
from gitcepter.log import error, info
from gitcepter.utils import version


def main():
    result = True

    env.is_server = False

    try:

        opts, args = getopt(sys.argv[1:], "hv")
        for op, value in opts:
            if op == '-h':
                usage()
                exit(0)
            elif op == '-v':
                print("gitcepter: " + version())
                exit(0)

        change = LocalChanges()

        # commit message
        message = open(sys.argv[1], "r").readline()
        info("执行commit规范检查...")
        result &= CommitMessageCheck(message).check()

        # checkstyle
        result &= Checkstyle(consts.checkstyle_config_xml, change.get_changed_java_files()).check()

        # json style
        info("执行json格式检查...")
        for file in change.get_changed_json_files():
            assert isinstance(file, ChangedFile)
            result &= JsonCheck(file_to_text(file.path)).check()

        # xml style
        info("执行xml格式检查...")
        for file in change.get_changed_xml_files():
            assert isinstance(file, ChangedFile)
            result &= XmlCheck(file_to_text(file.path)).check()

    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
        print("gitcepter:" + version())
        print(file=sys.stderr)
        print('An error occurred, but the commits are accepted.', file=sys.stderr)
        print_exc()
    if result:
        """ 0表示成功 """
        return 0
    """ 非0表示失败 """
    error("代码提交失败，请修正后重新提交")
    print("")
    return 1


def usage():
    pass
