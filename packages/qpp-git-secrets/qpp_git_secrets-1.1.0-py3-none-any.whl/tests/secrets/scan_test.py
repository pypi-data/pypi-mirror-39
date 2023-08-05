import re
from git_secrets.secrets import scan
from unidiff.patch import Line
from unittest.mock import patch


def test__scan_line():
    test_regex1 = re.compile('[dD]ogCow')
    test_regex2 = re.compile('[Mm]oof')
    test_regexes = [test_regex1, test_regex2]

    assert scan._scan_line(Line('I really like dogCows', '+'), test_regexes) is True
    assert scan._scan_line(Line('Dogcows go moof!', '+'), test_regexes) is True
    assert scan._scan_line(Line('Dogcows go MOOF!', '+'), test_regexes) is False


@patch('git_secrets.secrets.scan.cli_library', autospec=True)
@patch('git_secrets.secrets.scan.secrets', autospec=True)
def test_scan_with_zero_secrets(secrets_mock, cli_mock):
    secrets_mock.load_patterns.return_value = []

    scan.scan()

    cli_mock.fail_execution.assert_called_once_with(5,
                                                    'No secret patterns specified.  Specify secrets in .gitsecrets or '
                                                    '~/.gitsecrets')
