import click
from yo import pass_environment

from yo import cli


@cli.group()
def check():
    """commands to check now."""
    pass


@check.command()
@pass_environment
def now(ctx):
    """Welcome to yo."""
    about = """
 ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌       ▐░▌▐░░░░░░░░░░░▌
▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌
 ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌
     ▐░▌     ▐░▌       ▐░▌
     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌
     ▐░▌     ▐░░░░░░░░░░░▌
      ▀       ▀▀▀▀▀▀▀▀▀▀▀ 

Welcome to contribute your ideas.
https://github.com/tobyqin/yo
    """
    ctx.log(about, fg='green')


@check.command()
@pass_environment
def update(ctx):
    ctx.log("You are up to date!")
