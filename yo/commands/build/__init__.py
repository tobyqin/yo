import click
from .java import build as java_build


@click.group()
def build():
    """commands to build projects."""
    pass


@build.command()
def java():
    click.echo('yo, build java...')
    java_build()
