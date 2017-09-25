from pypif.util.serializable import Serializable

from citrination_client.search.core.query.data_query import DataQuery
from citrination_client.search.core.query.extraction_sort import ExtractionSort


class DataScope(Serializable):
    """
    Query to against data.
    """

    def __init__(self, query=None, extraction_sort=None, **kwargs):
        """
        Constructor.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        :param extraction_sort: A single :class:`ExtractionSort` object for sorting.
        """
        self._query = None
        self.query = query
        self._extraction_sort = None
        self.extraction_sort = extraction_sort

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(DataQuery, query)

    @query.deleter
    def query(self):
        self._query = None

    @property
    def extraction_sort(self):
        return self._extraction_sort

    @extraction_sort.setter
    def extraction_sort(self, extraction_sort):
        self._extraction_sort = self._get_object(ExtractionSort, extraction_sort)

    @extraction_sort.deleter
    def extraction_sort(self):
        self._extraction_sort = None
