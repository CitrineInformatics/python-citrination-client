from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery
from citrination_client.search.pif.query.core.file_reference_query import FileReferenceQuery
from citrination_client.search.pif.query.core.units_normalization import UnitsNormalization


class ValueQuery(BaseObjectQuery):
    """
    Class to query against a single value.
    """

    def __init__(self, name=None, value=None, file=None, units=None, units_normalization=None, logic=None,
                 extract_as=None, extract_all=None, extract_when_missing=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param name: One or more :class:`FieldQuery` operations against the name field.
        :param value: One or more :class:`FieldQuery` operations against the value.
        :param file: One or more :class:`FileReferenceQuery` operations against the file.
        :param units: One or more :class:`FieldQuery` operations against the units field.
        :param units_normalization: :class:`UnitsNormalization` object for normalizing units.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        super(ValueQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all,
                                         extract_when_missing=extract_when_missing, tags=tags,
                                         length=length, offset=offset)
        self._name = None
        self.name = name
        self._value = None
        self.value = value
        self._file = None
        self.file = file
        self._units = None
        self.units = units
        self._units_normalization = None
        self.units_normalization = units_normalization

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
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = self._get_object(FileReferenceQuery, file)

    @file.deleter
    def file(self):
        self._file = None

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = self._get_object(FieldQuery, units)

    @units.deleter
    def units(self):
        self._units = None

    @property
    def units_normalization(self):
        return self._units_normalization

    @units_normalization.setter
    def units_normalization(self, units_normalization):
        self._units_normalization = self._get_object(UnitsNormalization, units_normalization)

    @units_normalization.deleter
    def units_normalization(self):
        self._units_normalization = None
