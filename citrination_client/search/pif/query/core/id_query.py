from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class IdQuery(BaseObjectQuery):
    """
    Class to query against a PIF ID object.
    """
    
    def __init__(self, logic=None, simple=None, extract_as=None, extract_all=None, extract_when_missing=None, 
                 tags=None, length=None, offset=None, name=None, value=None, query=None, **kwargs):
        """
        Constructor.
        
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param simple: String with the query to run over all fields.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        :param name: One or more :class:`FieldQuery` operations against the name field.
        :param value: One or more :class:`FieldQuery` operations against the value field.
        :param query: One or more :class:`IdQuery` objects with nested queries.
        """
        super(IdQuery, self).__init__(
            logic=logic, simple=simple, extract_as=extract_as, extract_all=extract_all, 
            extract_when_missing=extract_when_missing, tags=tags, length=length, offset=offset, **kwargs)
        self._name = None
        self.name = name
        self._value = None
        self.value = value
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
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self._get_object(FieldQuery, value)

    @value.deleter
    def value(self):
        self._value = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(IdQuery, query)

    @query.deleter
    def query(self):
        self._query = None
