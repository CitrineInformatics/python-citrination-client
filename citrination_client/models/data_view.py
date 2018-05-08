class DataView(object):

    def __init__(self, view_id, name, description, datasets=[], column_names=[], columns=[]):
        """
        Constructor.

        :param view_id: The ID of the data view
        :type view_id: str
        :param name: The name of the data view
        :type name: str
        :param description: The description of the data view
        :type description: str
        :param datasets: The datasets used in the view
        :type datasets: list of :class: Dataset
        :param column_names: The column names in the view
        :type column_names: list of str
        """
        self._id = view_id
        self._name = name
        self._description = description
        self._datasets = datasets
        self._column_names = column_names
        self._columns = columns

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @id.deleter
    def id(self):
        self._id = None

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
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = value

    @datasets.deleter
    def datasets(self):
        self._datasets = None

    @property
    def column_names(self):
        return self._column_names

    @column_names.setter
    def column_names(self, value):
        self._column_names = value

    @column_names.deleter
    def column_names(self):
        self._column_names = None

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @columns.deleter
    def columns(self):
        self._columns = None
