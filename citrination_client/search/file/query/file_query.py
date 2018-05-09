from pypif.util.serializable import Serializable

from citrination_client.search.core.query.filter import Filter


class FileQuery(Serializable):
    """
    Class to store information about a file query.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, id=None, name=None, content=None,
                 updated_at=None, query=None, **kwargs):
        """
        Constructor.

        :param logic: The logic to apply to the query ('SHOULD', 'MUST', 'MUST_NOT', or 'OPTIONAL').
        :param weight: Weight for the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param id: One or more :class:`Filter` objects with filters against the id field.
        :param name: One or more :class:`Filter` objects with filters against the name field.
        :param content: One or more :class:`Filter` objects with filters against the content field.
        :param updated_at: One or more :class:`Filter` objects with filters against the time that the dataset was last updated.
        :param query: One or more :class:`DatasetQuery` objects with nested queries.
        """
        self._logic = None
        self.logic = logic
        self._weight = None
        self.weight = weight
        self._simple = None
        self.simple = simple
        self._simple_weight = None
        self.simple_weight = simple_weight
        self._id = None
        self.id = id
        self._name = None
        self.name = name
        self._content = None
        self.content = content
        self._updated_at = None
        self.updated_at = updated_at
        self._query = None
        self.query = query

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, logic):
        self._logic = logic

    @logic.deleter
    def logic(self):
        self._logic = None

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @weight.deleter
    def weight(self):
        self._weight = None

    @property
    def simple(self):
        return self._simple

    @simple.setter
    def simple(self, simple):
        self._simple = simple

    @simple.deleter
    def simple(self):
        self._simple = None

    @property
    def simple_weight(self):
        return self._simple_weight

    @simple_weight.setter
    def simple_weight(self, simple_weight):
        self._simple_weight = simple_weight

    @simple_weight.deleter
    def simple_weight(self):
        self._simple_weight = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = self._get_object(Filter, id)

    @id.deleter
    def id(self):
        self._id = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = self._get_object(Filter, name)

    @name.deleter
    def name(self):
        self._name = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = self._get_object(Filter, content)

    @content.deleter
    def content(self):
        self._content = None

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = self._get_object(Filter, updated_at)

    @updated_at.deleter
    def updated_at(self):
        self._updated_at = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(FileQuery, query)

    @query.deleter
    def query(self):
        self._query = None
