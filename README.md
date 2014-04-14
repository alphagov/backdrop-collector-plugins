# backdrop-collector-plugins

Plugins to work in conjunction with collectors for the alphagov/backdrop system.

An example configuration is given at the end of this document.

The basic form of a collector is like so:

```python
documents = get_documents_from_somewhere()

... magic happens ...

send_documents_to_backdrop(documents)
```

This package is a part of the `... magic happens ...`. To extend it, add your
code in the [`plugins` directory](https://github.com/alphagov/backdrop-collector-plugins/tree/master/backdrop/collector/plugins), import the relevant symbols in
the [`__init__.py`](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/__init__.py)
and [send a pull request](https://github.com/alphagov/backdrop-collector-plugins/compare/).

# Caveat

In the `backdrop-ga-collector`, if plugins are used, the final plugin *must*
be `ComputeIdFrom` at the moment, and this is likely to be true for a while.

This is because only the person writing plugin sequence can really know
what makes records unique.

# Installation

This module stands alone and is pip installable, but not currently on PyPi.

# Tests

Indirection is painful and the tests are small, so they live in the same module
as the code they are testing. Nosetests find them by virtual of the
[`--all-modules`](https://github.com/alphagov/backdrop-collector-plugins/blob/master/setup.cfg)
configuration option. If anyone disagrees strongly with this arrangement, a
pull request is welcome to fix it.

Tests are run on [travis-ci](https://travis-ci.org).

# Available plugins

Plugins are arbitrary [python expressions](http://docs.python.org/2/reference/expressions.html),
which are evaluated in the `backdrop.collector.plugins` namespace. They return a
callable which accepts a list of dictionaries and returns a list of dictionaries.

Plugins can do whatever they like to those dictionaries and the resulting list,
including modifying them in place or discarding some. This allows for
aggregation and discarding records.

The [plugin loading mechanism is very simple](https://github.com/alphagov/backdrop-collector-plugins/blob/4dc1adadfcb3288de766a1ee579996d2476ca6dc/backdrop/collector/plugins/load_plugin.py#L21)
and if in doubt you should take a look at how it and other example plugins
work.

## [ComputeDepartmentKey](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/department.py)	('variable name')

Computes a `department` field based on the contents of the given variable name.

## [ComputeIdFrom](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/compute_id.py)('varname1', [varname2]...)

Recomputes the `_id` and `humanId` fields from the specified 

## [RemoveKey](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/remove_key.py)('varname1', [varname2]...)

Delete the given keys from all documents.

## [AggregateKey](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/aggregate.py)(aggregation_func('varname1'), [a_f('varname2')]...)

Aggregates the given values according to the given `aggregation_func` where
`aggregation_func` might be `aggregate_count('varname')` which sums 'varname',
or `aggregate_rate('rate_varname', 'count_varname')` which can be used to
combine records where `'rate_varname'` represent a rate (e.g, a bounce rate),
weighted according to an appropriate `'count_varname'`

## [Comment](https://github.com/alphagov/backdrop-collector-plugins/blob/master/backdrop/collector/plugins/comment.py)(args...)

Ignores its arguments, useful for putting comments into the list of plugins
to explain what they are doing.

# Example configuration

```json
{
  "dataType": "content_dashboard_visitors_count",
  "query": {
    "id": "ga:123456",
    "metrics": [
      "visitors"
    ],
    "dimensions": [
      "customVarValue9"
    ]
  },
  "target": {
    "url": "http://localhost:3039/data/foo/visitors-count",
    "token": "foo-bearer-token"
  },
  "plugins": [
    "ComputeDepartmentKey('customVarValue9')",
    "Comment('customVarValue9 must be removed from the document before aggregation')",
    "RemoveKey('_id', 'humanId', 'customVarValue9')",
    "AggregateKey(aggregate_count('visitors'))",
    "ComputeIdFrom('_timestamp', 'timeSpan', 'dataType', 'department')"
  ]
}
```