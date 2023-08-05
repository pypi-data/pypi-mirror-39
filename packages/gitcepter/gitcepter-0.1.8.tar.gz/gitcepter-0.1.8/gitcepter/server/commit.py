# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from subprocess import check_output

from gitcepter.changes import Changes, ChangedFile
from gitcepter.utils import git_exe_path


class CommitList(list, Changes):
    """Routines on a list of sequential commits"""
    ref_path = None

    def __init__(self, other, branch_name):
        super(CommitList, self).__init__(other)
        self.branch_name = branch_name
        self.changed_files = []

    def __str__(self):
        name = '{}..{}'.format(self[0], self[-1])
        if self.ref_path:
            name += ' ({})'.format(self.branch_name)
        return name

    def get_changed_files(self):
        """Return the list of added or modified files on a commit"""
        changed_files = []
        # 翻转commit顺序， 使得提交按时间顺序由后到先
        self.reverse()
        if not self.changed_files:
            for commit in self:
                commit_changes = commit.get_changed_files()
                assert isinstance(commit_changes, list)
                paths = [change.path for change in changed_files]
                for commit_change in commit_changes:
                    assert isinstance(commit_change, ChangedFile)
                    if commit_change.path not in paths:
                        changed_files.append(commit_change)
                # changed_files = list(set(commit.get_changed_files()).union(set(changed_files)))

        self.changed_files = changed_files
        return self.changed_files


class Commit(Changes):
    """Routines on a single commit"""
    null_commit_id = '0000000000000000000000000000000000000000'

    def __init__(self, commit_id, commit_list=None):
        self.commit_id = commit_id
        self.commit_list = commit_list
        self.content_fetched = False
        self.changed_files = []

    def __str__(self):
        return self.commit_id[:8]

    def __bool__(self):
        return self.commit_id != Commit.null_commit_id

    def __nonzero__(self):
        return self.__bool__()

    def __eq__(self, other):
        return isinstance(other, Commit) and self.commit_id == other.commit_id

    def get_new_commit_list(self, branch_name):
        """Get the list of parent new commits in order"""
        output = check_output([
            git_exe_path,
            'rev-list',
            self.commit_id,
            '--not',
            '--all',
            '--reverse',
        ]).decode('utf-8')
        commit_list = CommitList([], branch_name)
        for commit_id in output.splitlines():
            commit = Commit(commit_id, commit_list)
            commit_list.append(commit)
        return commit_list

    def _fetch_content(self):
        content = check_output(
            [git_exe_path, 'cat-file', '-p', self.commit_id]
        )
        self._parents = []
        self._message_lines = []
        # The commit message starts after the empty line.  We iterate until
        # we find one, and then consume the rest as the message.
        lines = iter(content.splitlines())
        for line in lines:
            if not line:
                break
            if line.startswith(b'parent '):
                self._parents.append(Commit(line[len(b'parent '):].rstrip()))
            elif line.startswith(b'author '):
                self._author = Contributor.parse(line[len(b'author '):])
            elif line.startswith(b'committer '):
                self._committer = Contributor.parse(line[len(b'committer '):])
        for line in lines:
            self._message_lines.append(line.decode('utf-8'))
        self.content_fetched = True

    def get_parents(self):
        if not self.content_fetched:
            self._fetch_content()
        return self._parents

    def get_author(self):
        if not self.content_fetched:
            self._fetch_content()
        return self._author

    def get_committer(self):
        if not self.content_fetched:
            self._fetch_content()
        return self._committer

    def get_contributors(self):
        yield self.get_author()
        yield self._committer

    def get_message_lines(self):
        if not self.content_fetched:
            self._fetch_content()
        return self._message_lines

    def get_summary(self):
        return self.get_message_lines()[0]

    def parse_tags(self):
        tags = []
        rest = self.get_summary()
        while rest.startswith('[') and ']' in rest:
            end_index = rest.index(']')
            tags.append(rest[1:end_index])
            rest = rest[end_index + 1:]
        return tags, rest

    def content_can_fail(self):
        return not any(
            t in ['HOTFIX', 'MESS', 'TEMP', 'WIP']
            for t in self.parse_tags()[0]
        )

    def get_changed_files(self):
        """Return the list of added or modified files on a commit"""
        if not self.changed_files:
            output = check_output([
                git_exe_path,
                'diff-tree',
                '-r',
                '--root',  # Get the initial commit as additions
                '--no-commit-id',  # We already know the commit id.
                '--break-rewrites',  # Get rewrites as additions
                '--no-renames',  # Get renames as additions
                '--diff-filter=AM',  # Only additions and modifications
                self.commit_id,
            ]).decode('utf-8')
            changed_files = []
            for line in output.splitlines():
                line_split = line.split()
                assert len(line_split) == 6
                assert line_split[0].startswith(':')
                file_mode = line_split[1]
                file_path = line_split[5]
                changed_files.append(ChangedFile(file_path, self, file_mode))
            self.changed_files = changed_files
        return self.changed_files


class Contributor(object):
    """Routines on contribution properties of a commit"""

    def __init__(self, name, email, timestamp):
        self.name = name
        self.email = email
        self.timestamp = timestamp

    @classmethod
    def parse(cls, line):
        """Parse the contribution line as bytes"""
        name, line = line.split(b' <', 1)
        email, line = line.split(b'> ', 1)
        timestamp, line = line.split(b' ', 1)
        return cls(name.decode('utf-8'), email.decode('utf-8'), int(timestamp))

    def get_email_domain(self):
        return self.email.split('@', 1)[-1]
