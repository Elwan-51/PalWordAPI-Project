import importlib


class PluginInterface:
    """A plugin as a single function called initialisze"""

    @staticmethod
    def initialize(app) -> None:
        """Initialize the plugin"""


def import_module(name: str) -> PluginInterface:
    return importlib.import_module(name) # type: ignore


def load_plugins(plugins: list[str], app)-> None:
    """Load the plugins defined in the plugins list"""
    for plugins_name in plugins:
        plugin = import_module(plugins_name)
        plugin.initialize(app)