import click
from yo import pass_environment

from yo import cli


@cli.group(invoke_without_command=True)
@pass_environment
@click.argument('keyword', default='')
def search(env, keyword):
    """commands to check now."""
    if not keyword:
        click.launch('http://www.baidu.com')
    else:
        click.launch(f'http://www.baidu.com/s?wd={keyword}')
