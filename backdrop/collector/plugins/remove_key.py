
class RemoveKey(object):

    """
    Remove all of the specified keys from the input documents.
    """

    def __init__(self, *remove_keys):
        self.remove_keys = remove_keys

    def __call__(self, documents):
        return documents


def test_RemoveKey():
    from nose.tools import assert_equal

    doc = {"a": None, "b": None}

    plugin = RemoveKey("b")
    (output_doc,) = plugin([doc])

    expected_doc = {"a": None}
    assert_equal(expected_doc, output_doc)
