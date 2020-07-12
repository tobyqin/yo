from os import path
from pathlib import Path


class _Config():
    cli = None
    user_plugin_folder = Path.home() / 'yo/plugins'
    yo_dir = Path(path.dirname(__file__))
    yo_cli_module_name = 'commands'
    yo_cli_folder = yo_dir / yo_cli_module_name
    yo_plugin_example_folder = yo_dir / 'plugin_examples'
    yo_cli_internal = yo_cli_folder / 'internal'
    yo_cli_external = yo_cli_folder / 'external'
    yo_home = 'https://github.com/tobyqin/yo'


config = _Config()
