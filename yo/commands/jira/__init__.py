import click

from yo import cli
from yo import pass_environment
from yo.utils import get_jira_url, get_jira_id


@cli.group(invoke_without_command=True)
@click.pass_context
@pass_environment
def jira(env, ctx):
    """commands to work with jira."""
    assert isinstance(ctx, click.core.Context)
    if not ctx.invoked_subcommand:
        jira_url = get_jira_url(env.home)
        env.log('try to open default jira')
        click.launch(jira_url)


@jira.command()
@pass_environment
@click.argument('jira_id', default="")
def resolve(env, jira_id=""):
    if not jira_id:
        jira_id = get_jira_id(env.home)

    env.log(f'yo ~ resolve jira id: {jira_id}')
