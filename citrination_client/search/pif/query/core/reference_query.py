from citrination_client.search.pif.query.core.base_object_query import BaseObjectQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation
from citrination_client.search.pif.query.core.name_query import NameQuery
from citrination_client.search.pif.query.core.pages_query import PagesQuery


class ReferenceQuery(BaseObjectQuery):
    """
    Class used to query against a PIF Reference object.
    """

    def __init__(self, doi=None, isbn=None, issn=None, url=None, title=None, publisher=None, journal=None,
                 volume=None, issue=None, year=None, pages=None, authors=None, editors=None, affiliations=None,
                 acknowledgements=None, references=None, logic=None, tags=None, length=None, offset=None):
        """
        Constructor.

        :param doi: One or more :class:`FieldOperation` operations against the doi field.
        :param isbn: One or more :class:`FieldOperation` operations against the isbn field.
        :param issn: One or more :class:`FieldOperation` operations against the issn field.
        :param url: One or more :class:`FieldOperation` operations against the url field.
        :param title: One or more :class:`FieldOperation` operations against the title field.
        :param publisher: One or more :class:`FieldOperation` operations against the publisher field.
        :param journal: One or more :class:`FieldOperation` operations against the journal field.
        :param volume: One or more :class:`FieldOperation` operations against the volume field.
        :param issue: One or more :class:`FieldOperation` operations against the issue field.
        :param year: One or more :class:`FieldOperation` operations against the year field.
        :param pages: One or more :class:`PagesQuery` operations against the pages field.
        :param authors: One or more :class:`NameQuery` operations against the authors field.
        :param editors: One or more :class:`NameQuery` operations against the editors field.
        :param affiliations: One or more :class:`FieldOperation` operations against the affiliations field.
        :param acknowledgements: One or more :class:`FieldOperation` operations against the acknowledgements field.
        :param references: One or more :class:`ReferenceQuery` operations against the references field.
        :param logic: Logic for this filter. Must be equal to one of "MUST", "MUST_NOT", "SHOULD", or "OPTIONAL".
        :param tags: One or more :class:`FieldOperation` operations against the tags field.
        :param length: One or more :class:`FieldOperation` operations against the length field.
        :param offset: One or more :class:`FieldOperation` operations against the offset field.
        """
        super(ReferenceQuery, self).__init__(logic=logic, tags=tags, length=length, offset=offset)
        self._doi = None
        self.doi = doi
        self._isbn = None
        self.isbn = isbn
        self._issn = None
        self.issn = issn
        self._url = None
        self.url = url
        self._title = None
        self.title = title
        self._publisher = None
        self.publisher = publisher
        self._journal = None
        self.journal = journal
        self._volume = None
        self.volume = volume
        self._issue = None
        self.issue = issue
        self._year = None
        self.year = year
        self._pages = None
        self.pages = pages
        self._authors = None
        self.authors = authors
        self._editors = None
        self.editors = editors
        self._affiliations = None
        self.affiliations = affiliations
        self._acknowledgements = None
        self.acknowledgements = acknowledgements
        self._references = None
        self.references = references

    @property
    def doi(self):
        return self._doi

    @doi.setter
    def doi(self, doi):
        self._doi = self._get_object(FieldOperation, doi)

    @doi.deleter
    def doi(self):
        self._doi = None

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, isbn):
        self._isbn = self._get_object(FieldOperation, isbn)

    @isbn.deleter
    def isbn(self):
        self._isbn = None

    @property
    def issn(self):
        return self._issn

    @issn.setter
    def issn(self, issn):
        self._issn = self._get_object(FieldOperation, issn)

    @issn.deleter
    def issn(self):
        self._issn = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = self._get_object(FieldOperation, url)

    @url.deleter
    def url(self):
        self._url = None

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
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = self._get_object(FieldOperation, publisher)

    @publisher.deleter
    def publisher(self):
        self._publisher = None

    @property
    def journal(self):
        return self._journal

    @journal.setter
    def journal(self, journal):
        self._journal = self._get_object(FieldOperation, journal)

    @journal.deleter
    def journal(self):
        self._journal = None

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = self._get_object(FieldOperation, volume)

    @volume.deleter
    def volume(self):
        self._volume = None

    @property
    def issue(self):
        return self._issue

    @issue.setter
    def issue(self, issue):
        self._issue = self._get_object(FieldOperation, issue)

    @issue.deleter
    def issue(self):
        self._issue = None

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        self._year = self._get_object(FieldOperation, year)

    @year.deleter
    def year(self):
        self._year = None

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, pages):
        self._pages = self._get_object(PagesQuery, pages)

    @pages.deleter
    def pages(self):
        self._pages = None

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
    def editors(self):
        return self._editors

    @editors.setter
    def editors(self, editors):
        self._editors = self._get_object(NameQuery, editors)

    @editors.deleter
    def editors(self):
        self._editors = None

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

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, references):
        self._references = self._get_object(ReferenceQuery, references)

    @references.deleter
    def references(self):
        self._references = None
