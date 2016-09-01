from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation


class NameQuery(BaseObjectQuery):
    """
    Class to query against a Pif Name object.
    """

    def __init__(self, extract_as=None, given=None, family=None, title=None, suffix=None, logic=None, tags=None,
                 length=None, offset=None):
        """
        Constructor.

        :param extract_as: String with the name of field to extract the full name under.
        :param given: One or more :class:`FieldOperation` operations against the given name field.
        :param family: One or more :class:`FieldOperation` operations against the family name field.
        :param title: One or more :class:`FieldOperation` operations against the title field.
        :param suffix: One or more :class:`FieldOperation` operations against the suffix field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(NameQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._extract_as = None
        self.extract_as = extract_as
        self._given = None
        self.given = given
        self._family = None
        self.family = family
        self._title = None
        self.title = title
        self._suffix = None
        self.suffix = suffix

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
    def given(self):
        return self._given

    @given.setter
    def given(self, given):
        self._given = self._get_object(FieldOperation, given)

    @given.deleter
    def given(self):
        self._given = None

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, family):
        self._family = self._get_object(FieldOperation, family)

    @family.deleter
    def family(self):
        self._family = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = self._get_object(FieldOperation, title)

    @title.deleter
    def title(self):
        self._title = None

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        self._suffix = self._get_object(FieldOperation, suffix)

    @suffix.deleter
    def suffix(self):
        self._suffix = None
