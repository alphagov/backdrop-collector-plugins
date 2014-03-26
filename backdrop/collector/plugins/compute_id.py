import base64
import datetime

import pytz


def to_utc(a_datetime):
    return a_datetime.astimezone(pytz.UTC)


def value_id(value):
    value_bytes = value.encode('utf-8')
    return base64.urlsafe_b64encode(value_bytes), value_bytes


class ComputeIdFrom(object):

    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, documents):
        return documents


def stringify(item):
    if isinstance(item, datetime.datetime):
        return _format(item)
    return u"{0!s}".format(item)


def _format(timestamp):
    return to_utc(timestamp).strftime("%Y%m%d%H%M%S")


def test_ComputeIdFrom():
    from nose.tools import assert_in, assert_equal

    documents = [
        {"a": 1, "b": 2, "c": 3}
    ]

    plugin = ComputeIdFrom("a", "b")

    documents = plugin(documents)

    (document,) = documents

    assert_in("a", document)
    assert_in("b", document)

    assert_in("_id", document)
    assert_in("humanId", document)

    from pprint import pprint
    pprint(document)

    _id, humanId = value_id("{0}_{1}".format(document['a'], document['b']))
    assert_equal(_id, document['_id'])
    assert_equal(humanId, document['humanId'])

