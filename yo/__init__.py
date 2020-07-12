import os

import click

from yo.config import config
from yo.plugin_cli.loader import load_cli
from yo.utils import logger


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, verbose):
    """\b
 __   __  _______
|  | |  ||       |
|  |_|  ||   _   |
|       ||  | |  |
|_     _||  |_|  |
  |   |  |       |
  |___|  |_______|  Make life easy.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['home'] = os.getcwd()


config.cli = cli
load_cli()
