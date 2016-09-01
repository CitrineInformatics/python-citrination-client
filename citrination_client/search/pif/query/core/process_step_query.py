from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation
from citrination_client.search.pif.query.core.value_query import ValueQuery


class ProcessStepQuery(BaseObjectQuery):
    """
    Class to query against a process step.
    """

    def __init__(self, name=None, details=None, logic=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param name: One or more :class:`FieldOperation` operations against the name field.
        :param details: One or more :class:`ValueQuery` operations against the details of the step.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(ProcessStepQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._name = None
        self.name = name
        self._details = None
        self.details = details

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = self._get_object(FieldOperation, name)

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
