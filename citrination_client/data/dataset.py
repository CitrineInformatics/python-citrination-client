class Dataset(object):

    def __init__(self, id, name=None, description=None,
            created_at=None):
        self._name = name
        self._description = description
        self._id = id
        self._created_at = created_at

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at
