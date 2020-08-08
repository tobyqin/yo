import os
from pathlib import Path

from yo import config, logger


class CommandTypes():
    native = 'native'
    shell = 'shell'
    powershell = 'powershell'
    python = 'python'
    java = 'java'
    javascript = 'javascript'
    sql = 'sql'


class ICommand():

    def __init__(self):
        self.name = ''
        self.description = ''
        self.invoke = ''
        self.type = ''
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


class CommandGroup(ICommand):

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

        for cmd in self.commands:
            cmd.validate()

    def generate_cli(self, write_file=True):
        self.validate()

        def generate_imports():
            self.command_module_content += """
import os
import sys
import click
from yo.utils import logger,setup_yo_env
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
                self.command_module_content += f"""
@click.group(invoke_without_command=True)
@click.argument('args', nargs=-1)
def {self.name}(args):
    '''{self.better_comment()}'''
    ctx = click.get_current_context()
    if not ctx.invoked_subcommand:
        setup_yo_env('{self.from_plugin.name}')

        cmd = r'{self.invoke}'
        cmd += ' ' + ' '.join(args)
        os.system({_get_cmd_exec_prefix(self.type)}cmd)
"""

        def generate_commands():
            for cmd in self.commands:
                self.command_module_content += cmd.generate_cli(self.name)

        self.command_module_content = ''

        if self.type == CommandTypes.native:
            content = _get_native_plugin_module(self.invoke, self.from_plugin.from_dir)
            assert content, 'Not able to get native cli module!'
            self.command_module_content = content
        else:
            generate_imports()
            generate_group()
            generate_commands()

        if write_file:
            cli_module_path = config.yo_cli_external / f'{self.name}.py'
            config.yo_cli_external.mkdir(parents=True, exist_ok=True)
            cli_module_path.write_text(self.command_module_content)


class Command(ICommand):

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
        return f"""
@{group}.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1)
def {self.name}(args):
    '''{self.better_comment()}'''
    logger.vlog(r'Invoke: {self.invoke} ' + str(args) )
    setup_yo_env('{self.from_plugin.name}')

    cmd = r'{self.invoke}'
    cmd += ' ' + ' '.join(args)
    os.system({_get_cmd_exec_prefix(self.type)}cmd)
"""

    def validate(self):
        assert self.name, f'Invalid command name: {self.name}'
        assert self.invoke, f'No `invoke` found for command: {self.name}'


def _get_cmd_exec_prefix(cli_type: str):
    """command prefix will like: `python xxx.py` """
    if cli_type == CommandTypes.shell:
        return ''
    elif cli_type == CommandTypes.javascript:
        return '"node " + '
    else:
        return f'"{cli_type} " + '


def _get_native_plugin_module(invoke_target: str, plugin_dir: str):
    assert invoke_target, 'Should not be empty invoke target!'
    full_target = os.path.abspath(os.path.join(plugin_dir, invoke_target))
    if os.path.exists(full_target):
        return Path(full_target).read_text(encoding='utf8')
    else:
        logger.log(f'ERROR: not such invoke target: {full_target}!')
