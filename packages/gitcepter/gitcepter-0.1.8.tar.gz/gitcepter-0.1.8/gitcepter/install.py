import os
import sys
from getopt import getopt
from subprocess import check_output
from sys import stdout
from traceback import print_exc

from gitcepter import VERSION
from gitcepter.utils import version

dir_hook = 'hooks'
pre_receive = 'pre-receive'
pre_receive_backup = 'pre-receive.backup'

gitcepter_path = check_output(['type', 'gitcepter-server']).decode('utf-8').strip().split(" ")[2]


def main():
    deep = 0
    install = True
    try:
        opts, args = getopt(sys.argv[1:], "uvd:")
        for op, value in opts:
            if op == '-d':
                deep = int(value)
            elif op == '-u':
                install = False
            elif op == '-h':
                usage()
                exit(0)
            elif op == '-v':
                print("gitcepter-install: " + version())
                exit(0)

        if install:
            find_and_install(os.getcwd(), deep)
        else:
            find_and_uninstall(os.getcwd(), deep)

    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
        print("gitcepter-install: " + version())
        print(file=sys.stderr)
        print('An error occurred, but the commits are accepted.', file=sys.stderr)
        print_exc()


def find_and_install(parent, deep):
    # TODO 安装和卸载方式不够严谨
    deep = deep - 1
    files = os.listdir(parent)
    if dir_hook in files and os.path.isdir(parent):
        dir_hook_file = parent + os.sep + dir_hook
        pre_receive_file = dir_hook_file + os.sep + pre_receive
        pre_receive_backup_file = dir_hook_file + os.sep + pre_receive_backup
        if os.path.exists(pre_receive_backup_file):
            print("安装失败, 请检查gitcepter是否已经安装！")
            exit(1)

        print("gitcepter install: git repository " + os.path.abspath(pre_receive_file), end="... ")

        hooks = os.listdir(dir_hook_file)
        if pre_receive in hooks and os.path.isfile(pre_receive_file):
            os.rename(pre_receive_file, pre_receive_backup_file)
        os.symlink(gitcepter_path, pre_receive_file)
        print("install done")
    elif deep > 0:
        for file in files:
            suffix = os.path.splitext(file)[1]
            basename = os.path.basename(file)
            if os.path.isdir(file) and (suffix == '.git' or basename == '.git'):
                find_and_install(parent + os.path.sep + file, deep)


def find_and_uninstall(parent, deep):
    deep = deep - 1
    files = os.listdir(parent)
    if dir_hook in files and os.path.isdir(parent):
        dir_hook_file = parent + os.sep + dir_hook
        pre_receive_file = dir_hook_file + os.sep + pre_receive
        pre_receive_backup_file = dir_hook_file + os.sep + pre_receive_backup

        if os.path.exists(pre_receive_file):
            os.remove(pre_receive_file)
        if os.path.exists(pre_receive_backup_file):
            os.rename(pre_receive_backup_file, pre_receive_file)
            print("gitcepter uninstall: git repository " + pre_receive_file + "... uninstall done")
    elif deep > 0:
        for file in files:
            suffix = os.path.splitext(file)[1]
            basename = os.path.basename(file)
            if os.path.isdir(file) and (suffix == '.git' or basename == '.git'):
                find_and_uninstall(parent + os.path.sep + file, deep)


def usage():
    print("gitcepter-install [-u][-d deep][-h]")
    print("-u --> uninstall")
    print("-d --> search deep")
    print("-h --> print this usage")
