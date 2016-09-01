from pypif.util.serializable import Serializable


class Filter(Serializable):
    """
    Filter that can be applied to any field.
    """

    def __init__(self, logic=None, exists=None, equal=None, min=None, max=None, exact=None, filter=None):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param exists: True/False to simply test whether the field exists and has a non-null value.
        :param equal: String with the phrase to match against.
        :param min: String with the minimum value of a range to match against.
        :param max: String with the maximum value of a range to match against.
        :param exact: True/False to set whether the "equal" filter should be an exact match.
        :param filter: List of :class:`.Filter` objects with sub-filters.
        """
        self._logic = None
        self.logic = logic
        self._exists = None
        self.exists = exists
        self._equal = None
        self.equal = equal
        self._min = None
        self.min = min
        self._max = None
        self.max = max
        self._exact = None
        self.exact = exact
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
    def min(self):
        return self._min

    @min.setter
    def min(self, min):
        self._min = min

    @min.deleter
    def min(self):
        self._min = None

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max):
        self._max = max

    @max.deleter
    def max(self):
        self._max = None

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
    def exact(self):
        return self._exact

    @exact.setter
    def exact(self, exact):
        self._exact = exact

    @exact.deleter
    def exact(self):
        self._exact = None

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter):
        self._filter = self._get_object(Filter, filter)

    @filter.deleter
    def filter(self):
        self._filter = None
