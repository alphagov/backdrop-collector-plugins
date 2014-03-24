class ComputeDepartmentKey(object):
    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, documents):
        for document in documents:
            document["department"] = DEPARTMENT_MAPPING[document[self.key_name]]
        return documents

DEPARTMENT_MAPPING = {
    "<D1>": "Attorney General office",
    "<D2>": "CO",
    "<D3>": "BIS",
    "<D4>": "DCLG",
    "<D5>": "DCMS",
    "<D6>": "DfE",
    "<D7>": "Defra",
    "<D8>": "DFID",
    "<D9>": "DFT",
    "<D10>": "DWP",
    "<D11>": "DECC",
    "<D12>": "DH",
    "<D13>": "FCO",
    "<D15>": "HMT",
    "<D16>": "HO",
    "<D17>": "MoD",
    "<D18>": "MOJ",
    "<D25>": "HMRC",
    "<D102>": "FSA",
    "<OT532>": "No 10",
    "<OT537>": "ODPM",
}

FIXTURE = [
    {"key_name":"<D10>"},
    {"key_name":"<D18><D9>"},
    {"key_name":"<OT537>"},
    {"key_name":"<D30>"},]

def test_foo():
    from nose.tools import assert_equal, assert_in 

    plugin = ComputeDepartmentKey("key_name")
    documents = [{"key_name":"<D10>"}]
    (transformed_document, ) = plugin(documents)

    assert_in("department", transformed_document)
    assert_equal(transformed_document["department"], "DWP")

def test_fail_if_no_key_name_in_document():
    #assert_raises assertion_error
    pass