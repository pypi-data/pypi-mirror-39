

class JsonDocument(object):
    pk = None

    @property
    def label(self):
        raise NotImplementedError
