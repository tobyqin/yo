import click
from yo import pass_environment

from yo import cli


@cli.group()
def init():
    """commands to initialize projects."""
    pass


@init.command()
@click.confirmation_option()
@click.argument('type', default='java')
@pass_environment
def project(ctx, type):
    ctx.log(f'yo ~ init project: {type}')
    ctx.vlog(f'{ctx.home}')
