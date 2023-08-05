# -*- coding: utf-8 -*-
import abc
import os
from subprocess import check_output

from gitcepter import consts, env
from gitcepter.file import file_extension, save_file
from gitcepter.utils import git_exe_path


class ChangedFile(object):
    """Routines on a single committed file"""

    def __init__(self, path, commit=None, mode=None):
        self.path = path
        self.commit = commit
        assert mode is None or len(mode) == 6
        self.mode = mode
        self.content = None

    def __str__(self):
        return '{} at {}'.format(self.path, self.commit)

    def __eq__(self, other):
        return (
                isinstance(other, ChangedFile) and
                self.path == other.path and
                self.commit == other.commit
        )

    def exists(self):
        return bool(check_output([
            git_exe_path,
            'ls-tree',
            '--name-only',
            '-r',
            self.commit.commit_id,
            self.path,
        ]))

    def changed(self):
        return self in self.commit.get_changed_files()

    def regular(self):
        return self.mode[:2] == '10'

    def symlink(self):
        return self.mode[:2] == '12'

    def owner_can_execute(self):
        owner_bits = int(self.mode[-3])
        return bool(owner_bits & 1)

    def get_filename(self):
        return self.path.rsplit('/', 1)[-1]

    def get_file_parent(self):
        return os.path.split(self.path)[0]

    def get_extension(self):
        if '.' not in self.path:
            return None
        return self.path.rsplit('.', 1)[1]

    def get_content(self):
        """Get the file content as binary"""
        if self.content is None:
            self.content = check_output([
                git_exe_path, 'show', self.commit.commit_id + ':' + self.path
            ])
        return self.content

    def get_shebang(self):
        """Get the shebang from the file content"""
        if not self.regular():
            return None
        content = self.get_content()
        if not content.startswith(b'#!'):
            return None
        content = content[len(b'#!'):].strip()
        return content.split(None, 1)[0].decode('utf-8')

    def get_shebang_exe(self):
        """Get the executable from the shebang"""
        shebang = self.get_shebang()
        if not shebang:
            return None
        if shebang == '/usr/bin/env':
            rest = self.get_content().splitlines()[0][len(b'#!/usr/bin/env'):]
            rest_split = rest.split(None, 1)
            if rest_split:
                return rest_split[0].decode('utf-8')
        return shebang.rsplit('/', 1)[-1]


class Changes(object):
    java_files = []
    xml_files = []
    json_files = []
    has_category = False

    def __init__(self):
        pass

    def get_changed_java_files(self):
        if not self.java_files:
            self.category_files()
        return self.java_files

    def get_changed_xml_files(self):
        if not self.xml_files:
            self.category_files()
        return self.xml_files

    def get_changed_json_files(self):
        if not self.json_files:
            self.category_files()
        return self.json_files

    def category_files(self):
        if self.has_category:
            return
        for changed_file in self.get_changed_files():
            assert isinstance(changed_file, ChangedFile)
            extension = file_extension(changed_file.path)
            if extension == ".java":
                self.java_files.append(changed_file)
            elif extension == ".json":
                self.json_files.append(changed_file)
            elif extension == ".xml":
                self.xml_files.append(changed_file)

            if changed_file.path in [consts.checkstyle_exe_jar, consts.checkstyle_config_xml] and env.is_server:
                save_file(os.path.curdir, changed_file)
        self.has_category = True

    @abc.abstractmethod
    def get_changed_files(self):
        return []


class LocalChanges(Changes):

    def __init__(self):
        self.changed_files = None

    def get_changed_files(self):
        if self.changed_files:
            return self.changed_files
        output = check_output([
            git_exe_path,
            'diff',
            'HEAD',
            '--cached',
            '--name-only',
            '--diff-filter=ACMR'
        ]).decode('utf-8')
        changed_files = []
        for file_path in output.splitlines():
            changed_files.append(ChangedFile(file_path))
        self.changed_files = changed_files
        return self.changed_files

