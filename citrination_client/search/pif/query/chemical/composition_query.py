from citrination_client.search.pif.query.chemical.chemical_field_query import ChemicalFieldQuery
from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class CompositionQuery(BaseObjectQuery):
    """
    Class to query against a PIF Composition object.
    """

    def __init__(self, element=None, actual_weight_percent=None, actual_atomic_percent=None,
                 ideal_weight_percent=None, ideal_atomic_percent=None, logic=None, extract_as=None,
                 extract_all=None, extract_when_missing=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param element: One or more :class:`ChemicalFieldQuery` operations against the element field.
        :param actual_weight_percent: One or more :class:`FieldQuery` operations against the actual
        weight percent field.
        :param actual_atomic_percent: One or more :class:`FieldQuery` operations against the actual
        atomic percent field.
        :param ideal_weight_percent: One or more :class:`FieldQuery` operations against the ideal
        weight percent field.
        :param ideal_atomic_percent: One or more :class:`FieldQuery` operations against the ideal
        atomic percent field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        super(CompositionQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all,
                                               extract_when_missing=extract_when_missing, tags=tags, length=length,
                                               offset=offset)
        self._element = None
        self.element = element
        self._actual_weight_percent = None
        self.actual_weight_percent = actual_weight_percent
        self._actual_atomic_percent = None
        self.actual_atomic_percent = actual_atomic_percent
        self._ideal_weight_percent = None
        self.ideal_weight_percent = ideal_weight_percent
        self._ideal_atomic_percent = None
        self.ideal_atomic_percent = ideal_atomic_percent

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self._element = self._get_object(ChemicalFieldQuery, element)

    @element.deleter
    def element(self):
        self._element = None

    @property
    def actual_weight_percent(self):
        return self._actual_weight_percent

    @actual_weight_percent.setter
    def actual_weight_percent(self, actual_weight_percent):
        self._actual_weight_percent = self._get_object(FieldQuery, actual_weight_percent)

    @actual_weight_percent.deleter
    def actual_weight_percent(self):
        self._actual_weight_percent = None

    @property
    def actual_atomic_percent(self):
        return self._actual_atomic_percent

    @actual_atomic_percent.setter
    def actual_atomic_percent(self, actual_atomic_percent):
        self._actual_atomic_percent = self._get_object(FieldQuery, actual_atomic_percent)

    @actual_atomic_percent.deleter
    def actual_atomic_percent(self):
        self._actual_atomic_percent = None

    @property
    def ideal_weight_percent(self):
        return self._ideal_weight_percent

    @ideal_weight_percent.setter
    def ideal_weight_percent(self, ideal_weight_percent):
        self._ideal_weight_percent = self._get_object(FieldQuery, ideal_weight_percent)

    @ideal_weight_percent.deleter
    def ideal_weight_percent(self):
        self._ideal_weight_percent = None

    @property
    def ideal_atomic_percent(self):
        return self._ideal_atomic_percent

    @ideal_atomic_percent.setter
    def ideal_atomic_percent(self, ideal_atomic_percent):
        self._ideal_atomic_percent = self._get_object(FieldQuery, ideal_atomic_percent)

    @ideal_atomic_percent.deleter
    def ideal_atomic_percent(self):
        self._ideal_atomic_percent = None
