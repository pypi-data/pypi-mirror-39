from git_secrets.secrets import git


def test__run_git_with_arguments_good():
    assert git._run_git_with_arguments(['version']).startswith('git version')


def test__run_git_with_arguments_bad():
    assert 'is not a git command' in git._run_git_with_arguments(['not_a_real_git_sub_command'])
