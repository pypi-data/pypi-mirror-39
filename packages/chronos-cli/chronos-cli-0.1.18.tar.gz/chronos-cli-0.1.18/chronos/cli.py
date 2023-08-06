"""
Main entrypoint for chronos CLI.
"""

import argparse

from .semver import SemVer
from .helpers import (
    git_tags,
    last_git_release_tag,
    git_tag_to_semver,
    git_commits_since_last_tag,
    parse_commit_log,
    NoGitTagsException
)


def main(cmd_args: list = None) -> None:
    """
    :cmd_args: An optional list of command line arguments.

    Main function of chronos CLI tool.
    """
    parser = argparse.ArgumentParser(description='Auto-versioning utility.')
    subparsers = parser.add_subparsers()

    infer_parser = subparsers.add_parser('infer', help='infers next version')
    infer_parser.set_defaults(func=infer)

    commit_parser = subparsers.add_parser('commit', help='make release commit')
    commit_parser.set_defaults(func=commit)

    try:
        if cmd_args:
            args = parser.parse_args(cmd_args)
        else:
            args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()


def infer(args: argparse.Namespace) -> None:
    """
    :args: An argparse.Namespace object.

    This is the function called when the 'infer' sub-command is passed as an
    argument to the CLI.
    """
    try:
        last_tag = last_git_release_tag(git_tags())
    except NoGitTagsException:
        print(SemVer(0, 1, 0))
        exit(0)

    commit_log = git_commits_since_last_tag(last_tag)
    action = parse_commit_log(commit_log)

    last_ver: SemVer = git_tag_to_semver(last_tag)
    new_ver: SemVer = last_ver

    if action == 'min':
        new_ver.minor += 1
    elif action == 'maj':
        new_ver.major += 1
    else:
        new_ver.patch += 1

    print(new_ver)


def commit(args: argparse.Namespace) -> None:
    """
    :args: An argparse.Namespace object.

    This is the function called when the 'commit' sub-command is passed as an
    argument to the CLI.
    """
    print('Not implemented yet.')


if __name__ == '__main__':
    main()
