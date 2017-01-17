from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class PagesQuery(BaseObjectQuery):
    """
    Class to query against a Pif Pages object.
    """

    def __init__(self, start=None, end=None, logic=None, extract_as=None, extract_all=None, tags=None,
                 length=None, offset=None):
        """
        Constructor.

        :param start: One or more :class:`FieldOperation` operations against the starting page field.
        :param end: One or more :class:`FieldOperation` operations against the ending page field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(PagesQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all, tags=tags,
                                         length=length, offset=offset)
        self._start = None
        self.start = start
        self._end = None
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @start.deleter
    def start(self):
        self._start = None

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = self._get_object(FieldOperation, end)

    @end.deleter
    def end(self):
        self._end = None
