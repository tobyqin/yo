import os

from yo import config


class CommandTypes():
    native = 'native'
    shell = 'shell'
    powershell = 'powershell'
    python = 'python'
    java = 'java'
    javascript = 'javascript'
    typescript = 'typescript'
    sql = 'sql'


class CommandGroup():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.invoke = kwargs.get('invoke', None)
        self.type = kwargs.get('type', CommandTypes.shell)
        self.from_plugin = kwargs.get('from_plugin', None)
        self.commands = [Command.build(c, self.from_plugin) for c in kwargs.get('commands', [])]
        self.command_module_content = ''

    def __repr__(self):
        return str(self.__dict__)

    def build(cmd_group_kwargs: dict, from_plugin) -> 'CommandGroup':
        if cmd_group_kwargs:
            cmd_group_kwargs['from_plugin'] = from_plugin
            return CommandGroup(**cmd_group_kwargs)

    def generate_cli(self, write_file=True):

        def generate_imports():
            self.command_module_content += """
import os
import sys
import click
from yo.utils import logger
"""

        def generate_group():
            if not self.invoke:
                self.command_module_content += f"""
@click.group()
def {self.name}():
    '''{self.description}'''
    pass
"""
            else:
                invoke_target = build_invoke_target(self.invoke, self.from_plugin.from_dir)
                self.command_module_content += f"""
@click.group(invoke_without_command=True)
def {self.name}():
    '''{self.description}'''
    if not ctx.invoked_subcommand:
        os.system('{invoke_target}')
"""

        def generate_commands():
            for cmd in self.commands:
                self.command_module_content += cmd.generate_cli(self.name)

        generate_imports()
        generate_group()
        generate_commands()

        if write_file:
            cli_module_path = config.yo_plugin_external / f'{self.name}.py'
            cli_module_path.write_text(self.command_module_content)


class Command():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.invoke = kwargs.get('invoke', '')
        self.type = kwargs.get('type', CommandTypes.shell)
        self.from_plugin = kwargs.get('from_plugin', None)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def build(cmd_kwargs: dict, from_plugin) -> 'Command':
        if cmd_kwargs:
            cmd_kwargs['from_plugin'] = from_plugin
            return Command(**cmd_kwargs)

    def generate_cli(self, group):
        from yo.models.plugin import Plugin
        assert isinstance(self.from_plugin, Plugin)
        invoke_target = build_invoke_target(self.invoke, self.from_plugin.from_dir)
        return f"""
@{group}.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1)
def {self.name}(args):
    '''{self.description}'''
    logger.vlog(f'Invoke: {self.invoke} => {invoke_target} ' + str(args) )
    cmd = '{invoke_target} '
    cmd += ' '.join(args)
    os.system({get_cmd_exec_prefix(self.type)}cmd)
"""


def build_invoke_target(origin_invoke: str, plugin_dir: str):
    """Ensure the invoke target is correct."""
    assert origin_invoke, 'invoke target should not be empty!'
    cmd_parts = origin_invoke.split(' ')
    origin_target = cmd_parts[0]

    # if join origin invoke target with plugin folder exists, use it
    full_origin_target = os.path.abspath(os.path.join(plugin_dir, origin_target))
    if os.path.exists(full_origin_target):
        return origin_invoke.replace(origin_target, full_origin_target)

    # maybe it is a command in PATH or full path command, don't touch it
    else:
        return origin_invoke


def get_cmd_exec_prefix(cli_type: str):
    """command prefix will like: `python xxx.py` """
    if cli_type == CommandTypes.shell:
        return ''
    else:
        return f'"{cli_type} " + '
