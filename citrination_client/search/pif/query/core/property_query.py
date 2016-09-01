from citrination_client.search.pif.query.core.value_query import ValueQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class PropertyQuery(ValueQuery):
    """
    Class to query against a single property.
    """

    def __init__(self, conditions=None, data_type=None, name=None, value=None, units=None, units_normalization=None,
                 logic=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param conditions: One or more :class:`ValueQuery` operations against the conditions.
        :param data_type: One or more :class:`FieldOperation` operations against the dataType field.
        :param name: One or more :class:`FieldOperation` operations against the name field.
        :param value: One or more :class:`FieldOperation` operations against the value.
        :param units: One or more :class:`FieldOperation` operations against the units field.
        :param units_normalization: :class:`UnitsNormalization` object for normalizing units.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(PropertyQuery, self).__init__(name=name, value=value, units=units,
                                            units_normalization=units_normalization, logic=logic, tags=tags,
                                            length=length, offset=offset)
        self._conditions = None
        self.conditions = conditions
        self._data_type = None
        self.data_type = data_type

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
        self._data_type = self._get_object(FieldOperation, data_type)

    @data_type.deleter
    def data_type(self):
        self._data_type = None
