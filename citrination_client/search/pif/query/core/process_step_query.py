from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery
from citrination_client.search.pif.query.core.value_query import ValueQuery


class ProcessStepQuery(BaseObjectQuery):
    """
    Class to query against a process step.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None,  tags=None, length=None, offset=None, name=None, details=None,
                 query=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight of the query.
        :param simple: String with the query to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        :param name: One or more :class:`FieldQuery` operations against the name field.
        :param details: One or more :class:`ValueQuery` operations against the details of the step.
        :param query: One or more :class:`ProcessStepQuery` objects with nested queries.
        """
        super(ProcessStepQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._name = None
        self.name = name
        self._details = None
        self.details = details
        self._query = None
        self.query = query

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = self._get_object(FieldQuery, name)

    @name.deleter
    def name(self):
        self._name = None

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, details):
        self._details = self._get_object(ValueQuery, details)

    @details.deleter
    def details(self):
        self._details = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(ProcessStepQuery, query)

    @query.deleter
    def query(self):
        self._query = None
