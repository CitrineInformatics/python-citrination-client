from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class PagesQuery(BaseObjectQuery):
    """
    Class to query against a Pif Pages object.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, start=None, end=None,
                 query=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight of the query.
        :param simple: String with the simple query to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        :param start: One or more :class:`FieldQuery` operations against the starting page field.
        :param end: One or more :class:`FieldQuery` operations against the ending page field.
        :param query: One or more :class:`PagesQuery` objects with nested queries.
        """
        super(PagesQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._start = None
        self.start = start
        self._end = None
        self.end = end
        self._query = None
        self.query = query

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @start.deleter
    def start(self):
        self._start = None

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = self._get_object(FieldQuery, end)

    @end.deleter
    def end(self):
        self._end = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(PagesQuery, query)

    @query.deleter
    def query(self):
        self._query = None
