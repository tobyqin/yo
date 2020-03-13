from yo.cli import cli
import click

@cli.command()
def run():
    click.echo('build java')