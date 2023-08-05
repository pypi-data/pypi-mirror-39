import re
from git_secrets.secrets import scan
from unidiff.patch import Line


def test__scan_line():
    test_regex1 = re.compile('[dD]ogCow')
    test_regex2 = re.compile('[Mm]oof')
    test_regexes = [test_regex1, test_regex2]

    assert scan._scan_line(Line('I really like dogCows', '+'), test_regexes) is True
    assert scan._scan_line(Line('Dogcows go moof!', '+'), test_regexes) is True
    assert scan._scan_line(Line('Dogcows go MOOF!', '+'), test_regexes) is False
