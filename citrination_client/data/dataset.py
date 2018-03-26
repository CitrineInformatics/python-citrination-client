class Dataset(object):
    """
    Class representation of a dataset on Citrination.
    """

    def __init__(self, id, name=None, description=None,
            created_at=None):
        """
        Constructor.

        :param id: The ID of the dataset (required for instantiation)
        :type id: int
        :param name: The name of the dataset
        :type name: str
        :param description: The description of the dataset
        :type description: str
        :param created_at: The timestamp for creation of the dataset
        :type created_at: str
        """
        self._name = name
        self._description = description
        self._id = id
        self._created_at = created_at

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        self._name = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @description.deleter
    def description(self):
        self._description = None

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @created_at.deleter
    def created_at(self):
        self._created_at = None
