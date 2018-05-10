from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_query import FieldQuery


class FileReferenceQuery(BaseObjectQuery):
    """
    Class to query against a Pif FileReference object.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, extract_as=None, extract_all=None,
                 extract_when_missing=None, tags=None, length=None, offset=None, relative_path=None,
                 mime_type=None, sha256=None, md5=None, query=None, **kwargs):
        """
        Constructor.

        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param weight: Weight of the query.
        :param simple: String with the simple query to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param extract_as: String with the alias to save this field under.
        :param extract_all: Boolean setting whether all values in an array should be extracted.
        :param extract_when_missing: Any valid JSON-supported object or PIF object. This value is returned when a value is missing that should be extracted (and the overall query is still satisfied).
        :param tags: One or more :class:`FieldQuery` operations against the tags field.
        :param length: One or more :class:`FieldQuery` operations against the length field.
        :param offset: One or more :class:`FieldQuery` operations against the offset field.
        :param relative_path: One or more :class:`FieldQuery` operations against the relative path field.
        :param mime_type: One or more :class:`FieldQuery` operations against the mime type field.
        :param sha256: One or more :class:`FieldQuery` operations against the sha256 field.
        :param md5: One or more :class:`FieldQuery` operations against the md5 field.
        :param query: One or more :class:`FileReferenceQuery` objects as nested queries.
        """
        super(FileReferenceQuery, self).__init__(
            logic=logic, weight=weight, simple=simple, simple_weight=simple_weight, extract_as=extract_as,
            extract_all=extract_all, extract_when_missing=extract_when_missing, tags=tags, length=length,
            offset=offset, **kwargs)
        self._relative_path = None
        self.relative_path = relative_path
        self._mime_type = None
        self.mime_type = mime_type
        self._sha256 = None
        self.sha256 = sha256
        self._md5 = None
        self.md5 = md5
        self._query = None
        self.query = query

    @property
    def relative_path(self):
        return self._relative_path

    @relative_path.setter
    def relative_path(self, relative_path):
        self._relative_path = self._get_object(FieldQuery, relative_path)

    @relative_path.deleter
    def relative_path(self):
        self._relative_path = None

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type):
        self._mime_type = self._get_object(FieldQuery, mime_type)

    @mime_type.deleter
    def mime_type(self):
        self._mime_type = None

    @property
    def sha256(self):
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        self._sha256 = self._get_object(FieldQuery, sha256)

    @sha256.deleter
    def sha256(self):
        self._sha256 = None

    @property
    def md5(self):
        return self._md5

    @md5.setter
    def md5(self, md5):
        self._md5 = self._get_object(FieldQuery, md5)

    @md5.deleter
    def md5(self):
        self._md5 = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(FileReferenceQuery, query)

    @query.deleter
    def query(self):
        self._query = None
