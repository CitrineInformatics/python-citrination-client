from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class SourceQuery(BaseObjectQuery):
    """
    Class to query against a PIF Source object.
    """

    def __init__(self, producer=None, url=None, logic=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param producer: One or more :class:`FieldOperation` operations against the producer field.
        :param url: One or more :class:`FieldOperation` operations against the url field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(SourceQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._producer = None
        self.producer = producer
        self._url = None
        self.url = url

    @property
    def producer(self):
        return self._producer

    @producer.setter
    def producer(self, producer):
        self._producer = self._get_object(FieldOperation, producer)

    @producer.deleter
    def producer(self):
        self._producer = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = self._get_object(FieldOperation, url)

    @url.deleter
    def url(self):
        self._url = None
