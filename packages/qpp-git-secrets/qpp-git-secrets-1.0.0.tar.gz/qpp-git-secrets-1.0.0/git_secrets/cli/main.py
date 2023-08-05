import click
from . import scan
from . import install


@click.group()
def cli():
    pass


cli.add_command(scan.scan)
cli.add_command(install.install)
