
class ComputeRank(object):

    def __init__(self, var_name):
        self.var_name = var_name

    def __call__(self, documents):
        return documents

def test_rank():
    plugin = ComputeRank("rank")

    docs = [{}, {}]

    result = plugin(docs)

    doc1, doc2 = result

    assert doc1["rank"] == 1
    assert doc2["rank"] == 2