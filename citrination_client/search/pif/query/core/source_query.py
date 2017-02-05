from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class SourceQuery(BaseObjectQuery):
    """
    Class to query against a PIF Source object.
    """

    def __init__(self, producer=None, url=None, logic=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param producer: One or more :class:`FieldQuery` operations against the producer field.
        :param url: One or more :class:`FieldQuery` operations against the url field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value
        is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        """
        super(SourceQuery, self).__init__(logic=logic, extract_as=extract_as, extract_all=extract_all,
                                          extract_when_missing=extract_when_missing, tags=tags, length=length,
                                          offset=offset)
        self._producer = None
        self.producer = producer
        self._url = None
        self.url = url

    @property
    def producer(self):
        return self._producer

    @producer.setter
    def producer(self, producer):
        self._producer = self._get_object(FieldQuery, producer)

    @producer.deleter
    def producer(self):
        self._producer = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = self._get_object(FieldQuery, url)

    @url.deleter
    def url(self):
        self._url = None
