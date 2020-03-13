import logging
import pkg_resources

import click

logger = logging.getLogger(__name__)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require('yo')[0].version
    print('yo version {}'.format(version))
    ctx.exit()


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
def sync():
    click.echo('sync...')