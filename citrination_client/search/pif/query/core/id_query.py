from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class IdQuery(BaseObjectQuery):
    """
    Class to query against a PIF ID object.
    """
    
    def __init__(self, name=None, value=None, logic=None, tags=None, length=None, offset=None):
        """
        Constructor.
        
        :param name: One or more :class:`FieldOperation` operations against the name field.
        :param value: One or more :class:`FieldOperation` operations against the value field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(IdQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._name = None
        self.name = name
        self._value = None
        self.value = value
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._get_object(FieldOperation, name)
    
    @name.deleter
    def name(self):
        self._name = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._get_object(FieldOperation, value)

    @value.deleter
    def value(self):
        self._value = None
