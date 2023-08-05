from git_secrets.secrets import secrets
from unittest.mock import patch, mock_open
import sys


@patch('builtins.open', new_callable=mock_open, read_data='DogCow\nMoof\n')
def test_load_patterns(open_mock):
    if sys.version[:3] == '3.6':
        # Python 3.6's mock_open doesn't support __iter__, so just nuke this test
        return

    secret_regexes = secrets.load_patterns()

    assert len(secret_regexes) == 4
