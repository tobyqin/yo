import os

from yo import config, logger


class CommandTypes():
    native = 'native'
    shell = 'shell'
    powershell = 'powershell'
    python = 'python'
    java = 'java'
    javascript = 'javascript'
    typescript = 'typescript'
    sql = 'sql'


class CommandBase():

    def __init__(self):
        self.description = None
        self.from_plugin = None

    def __repr__(self):
        return str(self.__dict__)

    def build(self, **kwargs):
        pass

    def validate(self, **kwargs):
        pass

    def generate_cli(self, **kwargs):
        pass

    def better_comment(self):
        if self.description:
            return f'{self.description} [{self.from_plugin.id()}]'
        else:
            author = f'by {self.from_plugin.author}' if self.from_plugin.author else ''
            return f'command from plugin: {self.from_plugin.id()} {author}'


class CommandGroup(CommandBase):

    def __init__(self, **kwargs):
        super(CommandGroup, self).__init__()
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '').strip()
        self.invoke = kwargs.get('invoke', '').strip()
        self.type = kwargs.get('type', CommandTypes.shell)
        self.from_plugin = kwargs.get('from_plugin', None)
        self.commands = [Command.build(c, self.from_plugin) for c in kwargs.get('commands', [])]
        self.command_module_content = ''

    def build(cmd_group_kwargs: dict, from_plugin) -> 'CommandGroup':
        if cmd_group_kwargs:
            cmd_group_kwargs['from_plugin'] = from_plugin
            return CommandGroup(**cmd_group_kwargs)

    def validate(self):
        self.name = self.name.strip()
        assert self.name and ' ' not in self.name, f'Invalid command name: {self}'

        if not self.description:
            logger.log(f'Warn: no description for: {self.name}')

        for cmd in self.commands:
            cmd.validate()

    def generate_cli(self, write_file=True):
        self.validate()

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
    '''{self.better_comment()}'''
    pass
"""
            else:
                invoke_target = build_invoke_target(self.invoke, self.from_plugin.from_dir)
                self.command_module_content += f"""
@click.group(invoke_without_command=True)
def {self.name}():
    '''{self.better_comment()}'''
    ctx = click.get_current_context()
    if not ctx.invoked_subcommand:
        cmd = '{invoke_target}'
        os.system({get_cmd_exec_prefix(self.type)}cmd)
"""

        def generate_commands():
            for cmd in self.commands:
                self.command_module_content += cmd.generate_cli(self.name)

        self.command_module_content = ''
        generate_imports()
        generate_group()
        generate_commands()

        if write_file:
            cli_module_path = config.yo_plugin_external / f'{self.name}.py'
            cli_module_path.write_text(self.command_module_content)


class Command(CommandBase):

    def __init__(self, **kwargs):
        super(Command, self).__init__()
        self.name = kwargs.get('name', '').strip()
        self.description = kwargs.get('description', '').strip()
        self.invoke = kwargs.get('invoke', '').strip()
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
    '''{self.better_comment()}'''
    logger.vlog(f'Invoke: {self.invoke} => {invoke_target} ' + str(args) )
    cmd = '{invoke_target} '
    cmd += ' '.join(args)
    os.system({get_cmd_exec_prefix(self.type)}cmd)
"""

    def validate(self):
        assert self.name, f'Invalid command name: {self.name}'
        assert self.invoke, f'No `invoke` found for command: {self.name}'

        if not self.description:
            logger.log(f'Warn: no description for: {self.name}')


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
