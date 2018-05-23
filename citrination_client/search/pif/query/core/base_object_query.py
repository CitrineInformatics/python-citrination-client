from pypif.util.serializable import Serializable

from citrination_client.search.pif.query.core.field_query import FieldQuery


class BaseObjectQuery(Serializable):
    """
    Base class for all PIF object queries.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight for the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        self._logic = None
        self.logic = logic
        self._weight = None
        self.weight = weight
        self._simple = None
        self.simple = simple
        self._simple_weight = None
        self.simple_weight = simple_weight
        self._extract_as = None
        self.extract_as = extract_as
        self._extract_all = None
        self.extract_all = extract_all
        self._extract_when_missing = None
        self.extract_when_missing = extract_when_missing
        self._tags = None
        self.tags = tags
        self._length = None
        self.length = length
        self._offset = None
        self.offset = offset

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
    def simple(self):
        return self._simple

    @simple.setter
    def simple(self, simple):
        self._simple = simple

    @simple.deleter
    def simple(self):
        self._simple = None

    @property
    def simple_weight(self):
        return self._simple_weight

    @simple_weight.setter
    def simple_weight(self, simple_weight):
        self._simple_weight = simple_weight

    @simple_weight.deleter
    def simple_weight(self):
        self._simple_weight = None

    @property
    def extract_as(self):
        return self._extract_as

    @extract_as.setter
    def extract_as(self, extract_as):
        self._extract_as = extract_as

    @extract_as.deleter
    def extract_as(self):
        self._extract_as = None

    @property
    def extract_when_missing(self):
        return self._extract_when_missing

    @extract_when_missing.setter
    def extract_when_missing(self, extract_when_missing):
        self._extract_when_missing = extract_when_missing

    @extract_when_missing.deleter
    def extract_when_missing(self):
        self._extract_when_missing = None

    @property
    def extract_all(self):
        return self._extract_all

    @extract_all.setter
    def extract_all(self, extract_all):
        self._extract_all = extract_all

    @extract_all.deleter
    def extract_all(self):
        self._extract_all = None

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = self._get_object(FieldQuery, tags)

    @tags.deleter
    def tags(self):
        self._tags = None

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = self._get_object(FieldQuery, length)

    @length.deleter
    def length(self):
        self._length = None

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = self._get_object(FieldQuery, offset)

    @offset.deleter
    def offset(self):
        self._offset = None
