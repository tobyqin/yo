from yo.config import config
from yo.models.plugin import Plugin


def test_register_one_plugin():
    plugin_dir = config.user_plugin_folder / 'hello_cmd'
    plugin = Plugin.load_from(plugin_dir)
    plugin.validate()
    plugin.register()


def test_register_all_plugins():
    pass
