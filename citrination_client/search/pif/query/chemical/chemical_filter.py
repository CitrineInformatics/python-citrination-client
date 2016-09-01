from pypif.util.serializable import Serializable


class ChemicalFilter(Serializable):
    """
    Filter that can be applied to a field that stores chemical information.
    """

    def __init__(self, logic=None, exists=None, equal=None, element=None, partial=None, exact=None, filter=None):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param exists: True/False to simply test whether the field exists and has a non-null value.
        :param equal: String with the phrase to match against.
        :param element: True to match against the single element field.
        :param partial: True to match against the partial formula field.
        :param exact: True if matches should be exact.
        :param filter: List of :class:`ChemicalFilter` objects with sub-filters.
        """
        self._logic = None
        self.logic = logic
        self._exists = None
        self.exists = exists
        self._equal = None
        self.equal = equal
        self._element = None
        self.element = element
        self._partial = None
        self.partial = partial
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
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self._element = element

    @element.deleter
    def element(self):
        self._element = None

    @property
    def partial(self):
        return self._partial

    @partial.setter
    def partial(self, partial):
        self._partial = partial

    @partial.deleter
    def partial(self):
        self._partial = None

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
        self._filter = self._get_object(ChemicalFilter, filter)

    @filter.deleter
    def filter(self):
        self._filter = None
