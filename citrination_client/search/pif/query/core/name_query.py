from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class NameQuery(BaseObjectQuery):
    """
    Class to query against a Pif Name object.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, given=None, family=None,
                 title=None, suffix=None, query=None, **kwargs):
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
        :param given: One or more :class:`FieldQuery` operations against the given name field.
        :param family: One or more :class:`FieldQuery` operations against the family name field.
        :param title: One or more :class:`FieldQuery` operations against the title field.
        :param suffix: One or more :class:`FieldQuery` operations against the suffix field.
        :param query: One or more :class:`NameQuery` objects with nested queries.
        """
        super(NameQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._given = None
        self.given = given
        self._family = None
        self.family = family
        self._title = None
        self.title = title
        self._suffix = None
        self.suffix = suffix
        self._query = None
        self.query = query

    @property
    def given(self):
        return self._given

    @given.setter
    def given(self, given):
        self._given = self._get_object(FieldQuery, given)

    @given.deleter
    def given(self):
        self._given = None

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, family):
        self._family = self._get_object(FieldQuery, family)

    @family.deleter
    def family(self):
        self._family = None

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
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        self._suffix = self._get_object(FieldQuery, suffix)

    @suffix.deleter
    def suffix(self):
        self._suffix = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(NameQuery, query)

    @query.deleter
    def query(self):
        self._query = None
