from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation
from citrination_client.search.pif.query.core.name_query import NameQuery


class ReferenceQuery(BaseObjectQuery):
    """
    Class used to query against a PIF Reference object.
    """

    def __init__(self, title=None, authors=None, affiliations=None, acknowledgements=None, logic=None,
                 tags=None, length=None, offset=None):
        """
        Constructor.

        :param title: One or more :class:`FieldOperation` operations against the title field.
        :param authors: One or more :class:`NameQuery` operations against the authors field.
        :param affiliations: One or more :class:`FieldOperation` operations against the affiliations field.
        :param acknowledgements: One or more :class:`FieldOperation` operations against the acknowledgements field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(ReferenceQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._title = None
        self.title = title
        self._authors = None
        self.authors = authors
        self._affiliations = None
        self.affiliations = affiliations
        self._acknowledgements = None
        self.acknowledgements = acknowledgements

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
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, authors):
        self._authors = self._get_object(NameQuery, authors)

    @authors.deleter
    def authors(self):
        self._authors = None

    @property
    def affiliations(self):
        return self._affiliations

    @affiliations.setter
    def affiliations(self, affiliations):
        self._affiliations = self._get_object(FieldOperation, affiliations)

    @affiliations.deleter
    def affiliations(self):
        self._affiliations = None

    @property
    def acknowledgements(self):
        return self._acknowledgements

    @acknowledgements.setter
    def acknowledgements(self, acknowledgements):
        self._acknowledgements = self._get_object(FieldOperation, acknowledgements)

    @acknowledgements.deleter
    def acknowledgements(self):
        self._acknowledgements = None
