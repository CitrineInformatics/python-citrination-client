from pypif.util.serializable import Serializable

from citrination_client.search.core.query.data_query import DataQuery


class DataScope(Serializable):
    """
    Query to against data.
    """

    def __init__(self, query=None, **kwargs):
        """
        Constructor.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        """
        self._query = None
        self.query = query

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(DataQuery, query)

    @query.deleter
    def query(self):
        self._query = None
