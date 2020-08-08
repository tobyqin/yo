from os import path
from pathlib import Path


class _Config():
    cli = None
    yo_url = 'https://github.com/tobyqin/yo'

    user_folder = Path.home() / 'yo'
    user_plugin_dir = user_folder / 'plugins'
    current_plugin_dir = ''  # updated in runtime
    current_plugin_name = ''  # updated in runtime

    yo_dir = Path(path.dirname(__file__))
    yo_cli_module_name = 'commands'
    yo_cli_folder = yo_dir / yo_cli_module_name
    yo_plugin_example_dir = yo_dir / 'plugin_examples'
    yo_cli_internal = yo_cli_folder / 'internal'
    yo_cli_external = user_folder / 'commands'


config = _Config()
