from citrination_client.search.pif.query.chemical.chemical_filter import ChemicalFilter
from citrination_client.search.pif.query.core.base_field_query import BaseFieldQuery


class ChemicalFieldQuery(BaseFieldQuery):
    """
    Class for all field operations against chemical information.
    """

    def __init__(self, sort=None, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None,
                 extract_all=None, extract_when_missing=None, length=None, offset=None, filter=None, **kwargs):
        """
        Constructor.

        :param sort: ASCENDING or DESCENDING to set the sort order on this field.
        :param logic: Logic for this query. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight for the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param length: One or more :class:`FieldOperation` objects against the length field.
        :param offset: One or more :class:`FieldOperation` objects against the offset field.
        :param filter: One or more :class:`ChemicalFilter` objects against this field.
        """
        super(ChemicalFieldQuery, self).__init__(
            sort=sort, weight=weight, logic=logic, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, length=length, offset=offset, **kwargs)
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
