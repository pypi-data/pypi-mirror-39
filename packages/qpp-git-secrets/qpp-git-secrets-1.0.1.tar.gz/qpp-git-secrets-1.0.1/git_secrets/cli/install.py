import click
from ..secrets import install as internal


@click.command()
def install():
    internal.install()
