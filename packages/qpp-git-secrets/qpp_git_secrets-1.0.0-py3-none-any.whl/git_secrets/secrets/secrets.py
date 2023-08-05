from os import path
from typing import List, Pattern
import re


def load_patterns() -> List[Pattern[str]]:
    try:
        with open('.gitsecrets', 'r') as local_secrets:
            secrets = [line.strip() for line in local_secrets]
    except FileNotFoundError:
        try:
            with open(path.expanduser('~/.gitsecrets'), 'r') as user_secrets:
                secrets = [line.strip() for line in user_secrets]
        except FileNotFoundError:
            secrets = []

    secret_regexes = [re.compile(secret) for secret in secrets]

    return secret_regexes
