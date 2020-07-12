from pathlib import Path

from yo import cli
from yo.config import config
from yo.models.command import CommandGroup
from yo.models.plugin import Plugin
from yo.utils import logger, copy_and_overwrite

USER_PLUGIN_FOLDER = Path.home() / 'yo/plugins'


@cli.group()
def plugin():
    """commands to list and load plugins."""
    pass


@plugin.command()
def list():
    """list all plugins"""
    pass


@plugin.command()
def reload():
    """reload all plugins"""
    plugins = []
    cmd_groups = []
    if config.user_plugin_folder.exists():
        for plugin_folder in config.user_plugin_folder.glob('*'):
            if plugin_folder.is_dir():
                plugin = Plugin.load_from(plugin_folder)
                plugins.append(plugin)

    for plugin in plugins:
        assert isinstance(plugin, Plugin)
        plugin.validate()
        if plugin.error:
            logger.log(f'Failed to load {plugin.name}: {plugin.error}')
        else:
            logger.log(f'Loading plugin: {plugin.id()}')
            logger.vlog(f'Plugin detail: {plugin.__dict__}')
            cmd_groups = _merge_command_groups(cmd_groups, plugin.command_group_obj)

    logger.vlog(f'All command groups: {cmd_groups}')
    for cmd_group in cmd_groups:
        logger.log(f'Register command group: {cmd_group.name}')
        assert isinstance(cmd_group, CommandGroup)
        cmd_group.generate_cli()


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
