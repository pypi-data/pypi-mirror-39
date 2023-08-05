from typing import List, Optional
import subprocess
from unidiff import PatchSet
import os


def staged_diff() -> PatchSet:
    staged_diff_string = _run_git_with_arguments(['diff', '--staged', '-U0'])
    patch_set = PatchSet.from_string(staged_diff_string)

    return patch_set


def get_hooks_directory() -> Optional[str]:
    hooks_path = _run_git_with_arguments(['config', 'core.hooksPath'])
    if len(hooks_path) > 0:
        return hooks_path

    try:
        git_dir = os.environ['GIT_DIR']
        hooks_path = '{}/hooks/'.format(git_dir)
    except KeyError:
        hooks_path = ''
    if len(hooks_path) > 0:
        return hooks_path

    git_dir = _run_git_with_arguments(['rev-parse', '--git-dir'])
    if len(git_dir) > 0:
        return '{}/hooks/'.format(git_dir)

    return None


def _run_git_with_arguments(arguments: List[str]) -> str:
    return subprocess.check_output(['git'] + arguments, encoding='utf-8').strip()
