from pypif.util.serializable import Serializable

from citrination_client.search.core.query.boolean_filter import BooleanFilter
from citrination_client.search.core.query.filter import Filter


class DatasetQuery(Serializable):
    """
    Class to store information about a dataset query.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, id=None, is_featured=None,
                 name=None, description=None, owner=None, email=None, updated_at=None, query=None, **kwargs):
        """
        Constructor.

        :param logic: The logic to apply to the query ('SHOULD', 'MUST', 'MUST_NOT', or 'OPTIONAL').
        :param weight: Weight for the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param id: One or more :class:`Filter` objects with filters against the id field.
        :param is_featured:  One or more :class:`BooleanFilter` objects with filters against the isFeatured field.
        :param name: One or more :class:`Filter` objects with filters against the name field.
        :param description: One or more :class:`Filter` objects with filters against the description field.
        :param owner: One or more :class:`Filter` objects with filters against the owner field.
        :param email: One or more :class:`Filter` objects with filters against the email field.
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
        self._is_featured = None
        self.is_featured = is_featured
        self._name = None
        self.name = name
        self._description = None
        self.description = description
        self._owner = None
        self.owner = owner
        self._email = None
        self.email = email
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
    def is_featured(self):
        return self._is_featured

    @is_featured.setter
    def is_featured(self, is_featured):
        self._is_featured = self._get_object(BooleanFilter, is_featured)

    @is_featured.deleter
    def is_featured(self):
        self._is_featured = None

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
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = self._get_object(Filter, description)

    @description.deleter
    def description(self):
        self._description = None

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = self._get_object(Filter, owner)

    @owner.deleter
    def owner(self):
        self._owner = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = self._get_object(Filter, email)

    @email.deleter
    def email(self):
        self._email = None

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
        self._query = self._get_object(DatasetQuery, query)

    @query.deleter
    def query(self):
        self._query = None
