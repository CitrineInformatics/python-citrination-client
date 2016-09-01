from citrination_client.search.pif.query.chemical.chemical_filter import ChemicalFilter
from citrination_client.search.pif.query.core.base_field_operation import BaseFieldOperation


class ChemicalFieldOperation(BaseFieldOperation):
    """
    Class for all field operations against chemical information.
    """

    def __init__(self, filter=None, extract_as=None, length=None, offset=None):
        """
        Constructor.

        :param extract_as: String with the alias to save this field under.
        :param length: One or more :class:`.FieldOperation` objects against the length field.
        :param offset: One or more :class:`.FieldOperation` objects against the offset field.
        :param filter: One or more :class:`.ChemicalFilter` objects against this field.
        """
        super(ChemicalFieldOperation, self).__init__(extract_as=extract_as, length=length, offset=offset)
        self._filter = None
        self.filter = filter

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter):
        self._filter = self._get_object(ChemicalFilter, filter)

    @filter.deleter
    def filter(self):
        self._filter = None
