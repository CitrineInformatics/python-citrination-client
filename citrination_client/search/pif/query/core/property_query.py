from citrination_client.search.pif.query.core.field_query import FieldQuery
from citrination_client.search.pif.query.core.reference_query import ReferenceQuery
from citrination_client.search.pif.query.core.value_query import ValueQuery


class PropertyQuery(ValueQuery):
    """
    Class to query against a single property.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, conditions=None, data_type=None,
                 name=None, value=None, file=None, units=None, references=None, query=None, **kwargs):
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
        :param conditions: One or more :class:`ValueQuery` operations against the conditions.
        :param data_type: One or more :class:`FieldQuery` operations against the dataType field.
        :param name: One or more :class:`FieldQuery` operations against the name field.
        :param value: One or more :class:`FieldQuery` operations against the value.
        :param file: One or more :class:`FileReferenceQuery` operations against the file.
        :param units: One or more :class:`FieldQuery` operations against the units field.
        :param references: One or more :class:`ReferenceQuery` operations against the references field.
        :param query: One or more :class:`PropertyQuery` objects with nested queries.
        """
        super(PropertyQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, name=name, value=value, file=file, units=units, **kwargs)
        self._conditions = None
        self.conditions = conditions
        self._data_type = None
        self.data_type = data_type
        self._references = None
        self.references = references
        self._query = None
        self.query = query

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = self._get_object(ValueQuery, conditions)

    @conditions.deleter
    def conditions(self):
        self._conditions = None

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        self._data_type = self._get_object(FieldQuery, data_type)

    @data_type.deleter
    def data_type(self):
        self._data_type = None

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, references):
        self._references = self._get_object(ReferenceQuery, references)

    @references.deleter
    def references(self):
        self._references = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(PropertyQuery, query)

    @query.deleter
    def query(self):
        self._query = None
