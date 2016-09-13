from pypif.util.serializable import Serializable


class BaseFieldOperation(Serializable):
    """
    Base class for all field operations.
    """

    def __init__(self, extract_as=None, length=None, offset=None):
        """
        Constructor.

        :param extract_as: String with the alias to save this field under.
        :param length: One or more :class:`.FieldOperation` operations against the length field.
        :param offset: One or more :class:`.FieldOperation` operations against the offset field.
        """
        self._extract_as = None
        self.extract_as = extract_as
        self._length = None
        self.length = length
        self._offset = None
        self.offset = offset

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
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        from client.search.pif.query.core.field_operation import FieldOperation
        self._length = self._get_object(FieldOperation, length)

    @length.deleter
    def length(self):
        self._length = None

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        from client.search.pif.query.core.field_operation import FieldOperation
        self._offset = self._get_object(FieldOperation, offset)

    @offset.deleter
    def offset(self):
        self._offset = None
