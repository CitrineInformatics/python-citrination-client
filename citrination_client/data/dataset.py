class Dataset(object):
    """
    Class representation of a dataset on Citrination.
    """

    def __init__(self, id, name=None, description=None,
            created_at=None):
        """
        Constructor.

        :param id: The ID of the dataset (required for instantiation)
        :param name: The name of the dataset
        :param description: The description of the dataset
        :param created_at: The timestamp for creation of the dataset
        """
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
