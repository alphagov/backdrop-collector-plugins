from itertools import groupby


class AggregateKey(object):

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, documents):
        return documents


def group(iterable, key):
    for _, grouped in groupby(sorted(iterable, key=key), key=key):
        yield list(grouped)


def make_aggregate(docs, values_to_aggregate):
    """
    Given `docs` return a single document representing the aggregate
    """
    new_doc = dict(docs[0])

    def aggregation_function(docs):
        return sum(doc[keyname] for doc in docs)

    for keyname in values_to_aggregate:
        new_doc[keyname] = aggregation_function(docs)

    return new_doc


def aggregate_by_department(docs, values_to_aggregate=("pageviews",)):
    """
    Given `docs`, find all records with equal "key" where the "key" is all
    values which are
    """
    first = docs[0]

    aggregate = values_to_aggregate
    groupkeys = set(first) - set(aggregate)

    def key(doc):
        return tuple(doc[key] for key in groupkeys)

    return [make_aggregate(grouped, values_to_aggregate)
            for grouped in group(docs, key)]


def test_make_aggregate_sum():
    from nose.tools import assert_equal
    doc1 = {"a":2, "b":2, "c":2, "visits": 201}
    doc2 = {"a":2, "b":2, "c":2, "visits": 103}

    aggregate_doc = make_aggregate([doc1, doc2], ("visits", ))
    expected_aggregate = {"a":2, "b":2, "c":2, "visits": 304}
    assert_equal(aggregate_doc, expected_aggregate)

def test_make_aggregate_rate():
    pass