import os

import click

from yo.utils import pass_environment

enable_modules = ['init', 'build', 'jira']

# if set YO_DEBUG environment, will show the example commands
if os.environ.get('YO_DEBUG', 'false').lower() == 'true':
    enable_modules.append('example')


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(env, verbose):
    env.verbose = verbose


def dynamic_load():
    for module in enable_modules:
        group = getattr(__import__(f'yo.commands.{module}', None, None, [module]), module)
        cli.add_command(group)


def static_load():
    from yo.commands.build import build
    from yo.commands.example import example
    cli.add_command(example)
    cli.add_command(build)


dynamic_load()
