from os import path
from typing import List, Pattern
import re


def load_patterns() -> List[Pattern[str]]:
    try:
        with open('.gitsecrets', 'r') as local_secrets_file:
            local_secrets = [line.strip() for line in local_secrets_file]
    except FileNotFoundError:
        local_secrets = []
    try:
        with open(path.expanduser('~/.gitsecrets'), 'r') as user_secrets_file:
            user_secrets = [line.strip() for line in user_secrets_file]
    except FileNotFoundError:
        user_secrets = []

    secret_regexes = [re.compile(secret) for secret in local_secrets + user_secrets]

    return secret_regexes
