from pypif.util.serializable import Serializable
from citrination_client.search.dataset.query.dataset_query import DatasetQuery


class DatasetMultiQuery(Serializable):
    """
    Class to store information about a dataset multi-query.
    """

    def __init__(self, queries=None):
        """
        Constructor.

        :param queries: One or more :class:`.DatasetQuery` objects with the queries to run.
        """
        self._queries = None
        self.queries = queries

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, queries):
        self._queries = self._get_object(DatasetQuery, queries)

    @queries.deleter
    def queries(self):
        self._queries = None
