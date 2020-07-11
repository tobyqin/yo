from os import path
from pathlib import Path


class Config():
    cli = None
    user_plugin_folder = Path.home() / 'yo/plugins'
    yo_dir = Path(path.dirname(path.dirname(__file__)))
    yo_plugin_folder = yo_dir / 'plugins'
    yo_plugin_internal = yo_plugin_folder / 'internal'
    yo_plugin_external = yo_plugin_folder / 'external'
