import click

from ..secrets import scan as internal


@click.command()
def scan():
    internal.scan()
