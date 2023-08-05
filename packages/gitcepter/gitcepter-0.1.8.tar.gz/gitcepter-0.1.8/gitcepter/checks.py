# -*- coding: utf-8 -*-
import os
import re
from subprocess import check_output

from gitcepter.changes import ChangedFile
from gitcepter.file import file_exists
from gitcepter.log import info, error, warn
from gitcepter.utils import java_exe_path


class BaseCheck(object):

    def check(self):
        pass


class Checkstyle(BaseCheck):

    def __init__(self, config_file, java_files):
        self.config_file = config_file
        self.java_files = java_files

    def check(self):
        config_file = self.config_file
        if not self.config_file and not file_exists(config_file):
            """ 如果没有找到checkstyle配置文件,提示检查失败 """
            warn("configure file not exists: '" + config_file + "'")
            return False

        changed_java_files = self.java_files

        info("执行checkstyle检查...")
        is_dir = isinstance(changed_java_files, str) and os.path.isdir(changed_java_files)
        if not is_dir and len(changed_java_files) < 1:
            # print("没有java文件改动,已跳过checkstyle检查.")
            """ 如果没有java文件改动，直接跳过checkstyle检查 """
            return True

        args = [
            java_exe_path,
            '-jar',
            'libs/checkstyle.jar',
            '-c',
            config_file
        ]
        if is_dir:
            args.append(changed_java_files)
        else:
            for file in changed_java_files:
                assert isinstance(file, ChangedFile)
                args.append(file.path)

        print("command: " + " ".join(args))
        output = check_output(args).decode('utf-8')

        lines = output.splitlines()
        del lines[0]
        del lines[-1]

        if len(lines) > 0:
            for line in lines:
                print(line)
            error("checkstyle检查不通过,请检查后再执行commit")
            return False
        return True


class ContentCheck(BaseCheck):

    def __init__(self, content):
        self.content = content

    def check(self):
        pass


class JsonCheck(ContentCheck):

    def check(self):
        from json import loads
        try:
            loads(self.content)
        except Exception as e:
            error("json格式检查不通过:" + str(e))
            return False

        return True


class XmlCheck(ContentCheck):

    def check(self):
        from xml.etree import ElementTree
        try:
            ElementTree.fromstring(self.content)
        except Exception as e:
            error("xml格式检查不通过:" + str(e))
            return False
        return True


class CommitMessageCheck(ContentCheck):
    regex = "\[((bugfix\]\s{0,2}\[[a-zA-Z0-9_\-]{1,24})|crash|(feature\]\s{0,2}\[[a-zA-Z0-9_\-]{1," \
            "24})|docs|style|refactor|test|chore)\].+"

    def check(self):
        if not re.match(self.regex, self.content):
            error("不符合commit规范: " + self.content)
            error("""
    [bugfix][bug-id] comment						-->  bugfix
    [crash] comment									-->  线上crash
    [feature][feature-id] feature description		-->  新功能
    [docs]	 comment								-->  文档
    [style]   comment								-->  格式
    [refactor]	comment								-->  重构
    [test]  comment									-->  单元测试等测试代码
    [chore]  comment								-->  构建过程或辅助工具的变动""")
            return False
        return True
