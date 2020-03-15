import os
import sys

import click


class Environment(object):
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, **kwargs):
        """Logs a message."""
        click.secho(msg, **kwargs)

    def vlog(self, msg, **kwargs):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, **kwargs)


pass_environment = click.make_pass_decorator(Environment, ensure=True)


def get_jira_url(jira_id_str):
    return 'http://www.bing.com'


def get_jira_id(jira_id_str):
    return 'C123'

def get_bb_url(bb_str):
    return 'http://www.bing.com'
