"""
Load plugins to yo.
"""
from yo.config import config
from yo.utils import get_disable_plugins

DISABLE_PLUGINS = get_disable_plugins()


def load_plugins():
    load_internal_plugins()
    load_external_plugins()


def load_internal_plugins():
    plugins = _get_plugins(config.yo_plugin_internal)
    plugins = [p for p in plugins if p not in DISABLE_PLUGINS]
    _dynamic_load('yo.plugins.internal', plugins)


def load_external_plugins():
    plugins = _get_plugins(config.yo_plugin_external, as_single_file=True)
    print(plugins)
    _dynamic_load('yo.plugins.external', plugins)


def _get_plugins(plugin_folder, as_single_file=False):
    """get plugin module from internal plugin folder."""
    plugins = []
    for plugin_module in plugin_folder.glob('*'):
        if as_single_file:
            if plugin_module.is_file() \
                    and not plugin_module.name.startswith('_') \
                    and plugin_module.name.endswith('.py'):
                plugins.append(plugin_module.stem)
        elif plugin_module.is_dir() and not plugin_module.name.startswith('_'):
            plugins.append(plugin_module.stem)

    return plugins


def _dynamic_load(prefix, modules):
    """not very strong validation."""
    for module in modules:
        group = getattr(__import__(f'{prefix}.{module}', None, None, [module]), module)
        config.cli.add_command(group)
