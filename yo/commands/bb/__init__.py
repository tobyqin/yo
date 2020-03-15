import click

from yo import cli
from yo import pass_environment
from yo.utils import get_bb_url


@cli.group(invoke_without_command=True)
@click.pass_context
@pass_environment
def bb(env, ctx):
    """commands to work with bitbucket."""
    assert isinstance(ctx, click.core.Context)
    if not ctx.invoked_subcommand:
        bb_url = get_bb_url(env.home)
        env.log('try to open bb')
        click.launch(bb_url)
