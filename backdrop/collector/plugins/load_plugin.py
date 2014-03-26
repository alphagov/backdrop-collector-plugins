"""
load_plugin.py
--------------

Responsible for taking plugin strings and returning plugin callables.

"""

# For the linter
import __builtin__

import backdrop.collector.plugins

from backdrop.collector.plugins import AggregateKey, ComputeDepartmentKey


def load_plugins(plugin_names):
    return [load_plugin(plugin_name) for plugin_name in plugin_names]


def load_plugin(plugin_name):

    expr = compile(plugin_name, "backdrop.collector plugin", "eval")

    return eval(expr, __builtin__.__dict__,
                backdrop.collector.plugins.__dict__)


def test_load_plugin_trivial():
    from nose.tools import assert_equal

    assert_equal(1, load_plugin("1"))


def test_load_plugin_compute_department_key():
    from nose.tools import assert_is_instance

    plugin = load_plugin('ComputeDepartmentKey("customVarValue9")')
    assert_is_instance(plugin, ComputeDepartmentKey)


def test_load_plugin_compute_aggregate_key():
    from nose.tools import assert_is_instance

    plugin = load_plugin('AggregateKey(aggregate_count("visits"),'
                         '             aggregate_rate("rate", "visits"))')
    assert_is_instance(plugin, AggregateKey)
