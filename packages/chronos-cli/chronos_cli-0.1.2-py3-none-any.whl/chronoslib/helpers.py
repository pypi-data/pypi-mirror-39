"""
Helper functions for chronos CLI.
"""

import subprocess
from subprocess import CalledProcessError
import re

from .semver import SemVer
from .conventional_commits import patterns


class NoGitCommitSinceLastTagException(BaseException):
    """
    Exception meant to alert the user that their are no new commits since the
    last tag.
    """
    pass


class NonexistentGitTagError(ValueError):
    """
    Error meant to alert the user that the tag they have specified does not
    exist in the Git repository.
    """
    pass


class NoGitTagsException(BaseException):
    """
    Exception meant to alert the user that the repository does not contain any
    tags.
    """
    pass


def git_tags() -> str:
    """
    Calls `git tag --list --sort=-taggerdate` and returns the output as a UTF-8
    encoded string. Raises a NoGitTagsException if the repository doesn't
    contain any Git tags.
    """
    cmd = ['git', 'tag', '--list', '--sort=-taggerdate']
    rv = subprocess.check_output(cmd).decode('utf-8')

    if rv == '':
        raise NoGitTagsException('No Git tags are present in current repo.')

    return rv


def git_tag_to_semver(git_tag: str) -> SemVer:
    """
    :git_tag: A string representation of a Git tag.

    Searches a Git tag's string representation for a SemVer, and returns that
    as a SemVer object.
    """
    semver_re = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+$')
    ver_str = semver_re.search(git_tag)[0]

    return SemVer.from_str(ver_str)


def last_git_release_tag(git_tags: str) -> str:
    """
    :git_tags: `git tag --list` command output.

    Returns the latest Git tag ending with a SemVer as a string.
    """
    semver_re = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+$')
    str_ver = []
    for i in git_tags.split():
        if semver_re.search(i):
            str_ver.append(i)

    return str_ver[0]


def git_commits_since_last_tag(last_tag: str) -> dict:
    """
    Calls `git log` and returns the output as dict of hash-message pairs.
    """
    try:
        cmd = ['git', 'log', last_tag + '..', "--format='%H %s'"]
        rv: str = subprocess.check_output(cmd).decode('utf-8')
    except CalledProcessError:
        raise NonexistentGitTagError('No such tag:', last_tag)

    if not rv:
        raise NoGitCommitSinceLastTagException('No commits since last tag.')

    return rv


def parse_commit_log(commit_log: str) -> str:
    """
    :commit_log: `git log` output.

    Parse Git log and return either 'maj', 'min', or 'pat'.
    """
    rv: str = 'pat'

    if re.search(patterns()['feat'], commit_log):
        rv = 'min'

    if re.search(patterns()['BREAKING CHANGE'], commit_log):
        rv = 'maj'

    return rv
