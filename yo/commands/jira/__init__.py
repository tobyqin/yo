import click

from yo import cli
from yo import pass_environment


@cli.group(invoke_without_command=True)
@click.pass_context
@pass_environment
def jira(env, ctx):
    """commands to work with jira."""
    click.echo(f'{id(ctx)}, {dir(ctx)}')
    env.log('try to open default jira')


@jira.command()
@pass_environment
@click.argument('jira_id')
def goto(env, jira_id):
    env.log(f'yo ~ open jira id: {jira_id}')
