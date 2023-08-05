from . import secrets
from . import git
from unidiff import PatchedFile
from unidiff.patch import Line
from typing import List, Pattern
from ..cli import cli_library


def scan():
    secret_patterns = secrets.load_patterns()
    if len(secret_patterns) < 1:
        cli_library.fail_execution(5, 'No secret patterns specified.  Specify secrets in .gitsecrets or ~/.gitsecrets')

    diff = git.staged_diff()

    match = False

    for file_diff in diff:
        if _scan_diff_file(file_diff, secret_patterns):
            match = True

    if match:
        cli_library.fail_execution(2, 'Git secret violations exist')


def _scan_diff_file(file_diff: PatchedFile, patterns: List[Pattern[str]]) -> bool:
    match = False

    for chunk in file_diff:
        for line in chunk.target_lines():  # target_lines are new lines for the most part

            if not line.is_added:
                continue

            if _scan_line(line, patterns):
                cli_library.echo(
                    'Git secret violation at {}:{} -> {}'.format(file_diff.path, line.target_line_no, line.value))
                match = True

    return match


def _scan_line(line: Line, patterns: List[Pattern[str]]) -> bool:
    value = line.value
    overall_match = False

    for regex in patterns:
        match = regex.search(value)

        if match is not None:
            overall_match = True
            break

    return overall_match
