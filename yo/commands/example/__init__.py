import click

from yo.utils import pass_environment
import sys


@click.group(invoke_without_command=True)
@pass_environment
def example(env):
    """Example commands, enable by env YO_DEBUG=true"""
    ctx = click.get_current_context()  # get context
    assert isinstance(ctx, click.core.Context)
    if ctx.invoked_subcommand:
        env.log('Invoke example command now...')
    else:
        env.log('this is default group action')
        env.vlog(f'{id(ctx)}, {dir(ctx)}')


@example.command()
def baidu():
    """Open baidu in browser"""
    click.launch('http://www.baidu.com')


@example.command()
@pass_environment
@click.argument('name', default='toby')
def use_args(env, name):
    env.log(f'yo ~ name is {name}')


@example.command()
@pass_environment
@click.option('-d', '--debug', default=False)
def use_option(env, debug):
    env.log(f'yo ~ debug is {debug}')


@example.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1)
def multi_args(args):
    ctx = click.get_current_context()  # get context
    assert isinstance(ctx, click.core.Context)
    click.echo(sys.argv)
    click.echo(args)
