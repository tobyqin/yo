from pathlib import Path

from yo import cli
from yo.config import config
from yo.models.plugin import Plugin
from yo.plugin_cli.loader import get_external_cli, get_internal_cli
from yo.utils import logger, copy_and_overwrite, detail_error

USER_PLUGIN_FOLDER = Path.home() / 'yo/plugins'


@cli.group()
def plugin():
    """commands to list and load plugins."""
    pass


@plugin.command()
def list_cli():
    """list all cli modules"""
    internal_plugins = get_internal_cli()
    external_plugins = get_external_cli()

    output_result = 'External cli: \n'
    output_result += '\n'.join(external_plugins)
    output_result += '\n\nInternal cli:\n'
    output_result += '\n'.join(internal_plugins)
    logger.log(output_result)


@plugin.command()
def list():
    """list all installed plugins"""
    plugins = get_user_plugins()
    plugin_names = [p.id() for p in plugins]

    output_result = f'User plugins (from {config.user_plugin_folder}): \n'
    output_result += '\n'.join(plugin_names)
    logger.log(output_result)


@plugin.command()
def clear():
    """clear all registered plugins."""
    _clear_external_cli()


def get_user_plugins():
    plugins = []
    if config.user_plugin_folder.exists():
        for plugin_folder in config.user_plugin_folder.glob('*'):
            if plugin_folder.is_dir():
                plugin = Plugin.load_from(plugin_folder)
                plugins.append(plugin)

    return plugins


@plugin.command()
def reload():
    """reload all plugins"""
    _clear_external_cli(print_log=False)

    plugins = get_user_plugins()
    cmd_groups = []

    for plugin in plugins:
        load_info = f'Loading plugin: {plugin.id()} => '
        assert isinstance(plugin, Plugin)
        plugin.validate()
        if plugin.error:
            logger.log(f'{load_info}{plugin.error}')
        else:
            logger.log(f'{load_info}OK.')
            logger.vlog(f'Plugin detail: {plugin.__dict__}')
            cmd_groups = _merge_command_groups(cmd_groups, plugin.command_group_obj)

    logger.vlog(f'All command groups: {cmd_groups}')
    for cmd_group in cmd_groups:
        info = f'Register command group: {cmd_group.name} => '
        internal_cli = get_internal_cli()
        try:
            assert cmd_group.name not in internal_cli, f'Conflicted with internal commands: {internal_cli}'
            cmd_group.generate_cli()
            info += 'OK.'
        except Exception as e:
            info += detail_error(e)
        logger.log(info)


def _clear_external_cli(print_log=True):
    for _cli in config.yo_cli_external.glob('*.py'):
        if not _cli.stem.startswith('_'):
            if print_log:
                logger.log(f'Clear plugin command: {_cli.stem}')
            _cli.unlink()


def _merge_command_groups(cmd_group_list, cmd_group):
    logger.vlog(f'Mering command group: {cmd_group}')

    found_same_group = [x for x in cmd_group_list if x and x.name == cmd_group.name]
    merge_list = [x for x in cmd_group_list if x and x.name != cmd_group.name]

    if found_same_group:
        merged_group = _merge_cmd_obj(found_same_group[0], cmd_group.commands)
        merge_list.append(merged_group)
    else:
        merge_list.append(cmd_group)

    return merge_list


def _merge_cmd_obj(cmd_group, cmds):
    # TODO: should validate duplicate commands
    cmd_group.commands.extend(cmds)
    return cmd_group


@plugin.command()
def init():
    """Init user plugins directory."""
    logger.log(f'Initialize plugin directory: {config.user_plugin_folder}')
    config.user_plugin_folder.mkdir(parents=True, exist_ok=True)
    for example in config.yo_plugin_example_folder.glob('*'):
        _init_example(example.stem)


def _init_example(example_name):
    example_from = config.yo_plugin_example_folder / example_name
    example_to = config.user_plugin_folder / example_name
    logger.log(f'Init plugin example: {example_name} => {example_to}')
    copy_and_overwrite(str(example_from), str(example_to))
