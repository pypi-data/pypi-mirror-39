# -*- coding: utf-8 -*-
import sys
from getopt import getopt
from sys import stdout
from traceback import print_exc

from fileinput import input

from gitcepter import consts, env, VERSION
from gitcepter.changes import ChangedFile
from gitcepter.checks import Checkstyle, XmlCheck, JsonCheck, CommitMessageCheck
from gitcepter.file import mk_cache, save_file, rm_cache
from gitcepter.log import error
from gitcepter.server.commit import Commit
from gitcepter.utils import version


def main():
    result = True

    env.is_server = True

    try:
        opts, args = getopt(sys.argv[1:], "hv")
        for op, value in opts:
            if op == '-h':
                usage()
                exit(0)
            elif op == '-v':
                print("gitcepter-server: " + version())
                exit(0)

        for line in input():
            result &= process_line(line)
    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
        print("gitcepter-server: " + version())
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


def process_line(line):
    line_split = line.split()
    ref_path_split = line_split[2].split('/', 2)
    if ref_path_split[0] != 'refs' or len(ref_path_split) != 3:
        return

    commit = Commit(line_split[1])
    if not commit:
        # This is a delete.  We don't check anything on deletes.
        return
    if ref_path_split[1] == 'tags':
        return

    branch_name = ''
    if ref_path_split[1] == 'heads':
        branch_name = line_split[2]

    return process_commit(commit, branch_name)


def process_commit(latest_commit, branch_name):
    result = True

    commit_list = latest_commit.get_new_commit_list(branch_name)

    # commit规范检查
    for commit in commit_list:
        result &= CommitMessageCheck(commit.get_summary()).check()

    # checkstyle
    cache_dir = mk_cache("java")  # 创建缓存目录
    java_files = commit_list.get_changed_java_files()
    if len(java_files) > 0:
        for java_file in java_files:
            save_file(cache_dir, java_file)
        result &= Checkstyle(consts.checkstyle_config_xml, cache_dir).check()
    rm_cache()

    # xml 格式检查
    for xml_file in commit_list.get_changed_xml_files():
        assert isinstance(xml_file, ChangedFile)
        result &= XmlCheck(xml_file.get_content()).check()

    # json 格式检查
    for json_file in commit_list.get_changed_json_files():
        assert isinstance(json_file, ChangedFile)
        result &= JsonCheck(json_file.get_content()).check()
    return result


def usage():
    pass