class AggregateByKey(object):
    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, documents):
        return documents