"""
load_plugin.py
--------------

Responsible for taking plugin strings and returning plugin callables.

Examples of plugins:

    # Identity, does nothing
    `__builtins__:(lambda docs: docs)`

    # If `docs` were integers, this would sum them.
    `__builtins__:sum`

    `backdrop.collector.plugins:ComputeDepartment()`
    `backdrop.collector.plugins:AggregateKey()`

Strings consist of an (optional) module-part, a colon, and an expression-part.

If the string does not begin with something module-like ending in a `:`, then
it is assumed that the plugin resides in `backdrop.collector.plugins`.

The expression-part is evaluated with a local namespace of the module.
"""


def load_plugins(plugin_names):
    return [load_plugin(plugin_name) for plugin_name in plugin_names]


def load_plugin(plugin_name):
    pass


def test_load_plugin():
    pass


def parse_plugin_string(plugin_string):
    """
    Determine module-part and expression-part of `plugin_string`
    """

PLUGIN_PARSE_TESTS = [
    ["a.b.c:expression.foo", ("a.b.c", "expression.foo")],
    ["expression.foo", ("backdrop.collector.plugins", "expression.foo")],

    ['expression.foo("bar: baz")',
     ("backdrop.collector.plugins", 'expression.foo("bar: baz")')],

    ['module.foo:expression.foo("bar: baz")',
     ("module.foo", 'expression.foo("bar: baz")')],
]


def test_parse_plugin_string():
    from nose.tools import assert_equal

    def check(input_, expected):
        output = parse_plugin_string(input_)
        assert_equal(output, expected)

    for input_, expected in PLUGIN_PARSE_TESTS:
        yield check, input_, expected
