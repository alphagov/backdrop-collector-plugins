"""
load_plugin.py
--------------

Responsible for taking plugin strings and returning plugin callables.

"""


def load_plugins(plugin_names):
    return [load_plugin(plugin_name) for plugin_name in plugin_names]


def load_plugin(plugin_name):
    pass


def test_load_plugin():
    pass