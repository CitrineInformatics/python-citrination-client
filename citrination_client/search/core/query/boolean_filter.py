from pypif.util.serializable import Serializable


class BooleanFilter(Serializable):
    """
    Boolean filter that can be applied to any field.
    """

    def __init__(self, logic=None, weight=None, exists=None, equal=None, filter=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight for the filter.
        :param exists: True/False to simply test whether the field exists and has a non-null value.
        :param equal: String with the phrase to match against.
        :param filter: List of :class:`BooleanFilter` objects with sub-filters.
        """
        self._logic = None
        self.logic = logic
        self._weight = None
        self.weight = weight
        self._exists = None
        self.exists = exists
        self._equal = None
        self.equal = equal
        self._filter = None
        self.filter = filter

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, logic):
        self._logic = logic

    @logic.deleter
    def logic(self):
        self._logic = None

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @weight.deleter
    def weight(self):
        self._weight = None

    @property
    def exists(self):
        return self._exists

    @exists.setter
    def exists(self, exists):
        self._exists = exists

    @exists.deleter
    def exists(self):
        self._exists = None

    @property
    def equal(self):
        return self._equal

    @equal.setter
    def equal(self, equal):
        self._equal = equal

    @equal.deleter
    def equal(self):
        self._equal = None

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter):
        self._filter = self._get_object(BooleanFilter, filter)

    @filter.deleter
    def filter(self):
        self._filter = None
