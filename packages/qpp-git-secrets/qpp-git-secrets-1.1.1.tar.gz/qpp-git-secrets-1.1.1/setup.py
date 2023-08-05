from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', 'r') as read_me:
        long_description = read_me.read()
        return long_description


def get_requirements():
    requirements = open('requirements.txt').read()
    return [r for r in requirements.strip().splitlines()]


setup(
    name='qpp-git-secrets',
    version='1.1.1',
    author='halprin',
    author_email='me@halprin.io',
    description='Git without secrets',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/halprin/git-secrets',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=('tests',)),
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        git-secrets=git_secrets.cli.main:cli
    ''',
)
