from pathlib import Path

from yaml import full_load

from yo.models.command import CommandGroup


class Plugin():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.author = kwargs.get('author', '')
        self.description = kwargs.get('description', '')
        self.version = kwargs.get('version', '')
        self.enabled = kwargs.get('enabled', False)
        self.installed = kwargs.get('installed', False)
        self.is_internal = False  # we will have internal & external plugins
        self.error = ''  # record error when using this plugin
        self.command_group_raw = kwargs.get('command-group', None)  # commands provided by this plugin
        self.command_group_obj = None

    @staticmethod
    def load_from(plugin_dir: Path) -> 'Plugin':
        """load plugin from a directory"""
        plugin = Plugin()
        try:
            plugin_yaml = plugin_dir / 'plugin.yml'
            with open(str(plugin_yaml)) as f:
                plugin_info = full_load(f)
                plugin = Plugin(**plugin_info)
        except Exception as e:
            plugin.name = plugin_dir.stem
            plugin.error = str(e)

        return plugin

    def validate(self):
        """validate the plugin is ready to import."""
        try:
            self._build_command_group_obj()
        except Exception as e:
            self.error = str(e)

        return self.error == ''

    def _build_command_group_obj(self):
        """try to build the command group object."""
        self.command_group_obj = CommandGroup.build(self.command_group_raw)

    def deactivate(self):
        """deactivate the plugin, will clean it after deactivation."""

    def import_it(self):
        """import this plugin to plugins folder."""

    def clean_it(self):
        """clean this plugin in plugins folder."""

    def register(self):
        """register this plugin to system."""
        print(self.__dict__)


class PluginSettings():
    pass