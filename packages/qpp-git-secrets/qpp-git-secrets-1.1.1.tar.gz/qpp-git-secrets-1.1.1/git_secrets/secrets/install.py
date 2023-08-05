from . import git
from ..cli import cli_library
from os import path
import os
import stat


def install():
    hooks_directory = git.get_hooks_directory()
    if hooks_directory is None:
        cli_library.fail_execution(3, 'There is no hook directory')

    pre_commit_directory = path.join(hooks_directory, 'pre-commit.d')
    pre_commit_hook = path.join(hooks_directory, 'pre-commit')

    if path.isdir(pre_commit_directory):
        _create_hook('git-secrets.sh', pre_commit_directory)
    elif path.exists(pre_commit_hook):
        cli_library.fail_execution(4, "The pre-commit hook already exists.  You can manually scan by running 'git "
                                      "secrets scan'")
    else:
        _create_hook('pre-commit', hooks_directory)


def _create_hook(name: str, directory_path: str):
    hook_path = path.join(directory_path, name)

    with open(hook_path, 'w') as hook:
        hook.writelines(['#!/usr/bin/env bash\n', 'git secrets scan\n'])

    os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
