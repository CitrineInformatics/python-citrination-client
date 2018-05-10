from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class DisplayItemQuery(BaseObjectQuery):
    """
    Class to query against a Pif DisplayItem object.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, number=None, title=None,
                 caption=None, query=None, **kwargs):
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
        :param number: One or more :class:`FieldQuery` operations against the number field.
        :param title: One or more :class:`FieldQuery` operations against the title field.
        :param caption: One or more :class:`FieldQuery` operations against the caption field.
        :param query: One or more :class:`DisplayItemQuery` objects as nested queries.
        """
        super(DisplayItemQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._title = None
        self.title = title
        self._number = None
        self.number = number
        self._caption = None
        self.caption = caption
        self._query = None
        self.query = query

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = self._get_object(FieldQuery, number)

    @number.deleter
    def number(self):
        self._number = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = self._get_object(FieldQuery, title)

    @title.deleter
    def title(self):
        self._title = None

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        self._caption = self._get_object(FieldQuery, caption)

    @caption.deleter
    def caption(self):
        self._caption = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(DisplayItemQuery, query)

    @query.deleter
    def query(self):
        self._query = None
