from citrination_client.search.core.query.base_returning_query import BaseReturningQuery


class DatasetReturningQuery(BaseReturningQuery):
    """
    Query used to return information about datasets. Citrination does not support pagination past the 50,000th result. Please chose values for from_index and size that do not exceed this limit.
    """

    def __init__(self, query=None, from_index=None, size=None, random_results=None, random_seed=None,
                 score_relevance=None, return_max_score=None, timeout=None, count_pifs=None, **kwargs):
        """
        Constructor.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        :param from_index: Index of the first hit that should be returned.
        :param size: Total number of hits the should be returned.
        :param random_results: Whether to return a random set of records.
        :param random_seed: The random seed to use.
        :param score_relevance: Whether to use relevance scoring.
        :param return_max_score: Whether to return the maximum score.
        :param timeout: The number of milliseconds to wait for the query to execute.
        :param count_pifs: Whether to return counts of PIFs for each dataset.
        """
        super(DatasetReturningQuery, self).__init__(
            query=query, from_index=from_index, size=size, random_results=random_results, random_seed=random_seed,
            score_relevance=score_relevance, return_max_score=return_max_score, timeout=timeout, **kwargs)
        self._count_pifs = None
        self.count_pifs = count_pifs

    @property
    def count_pifs(self):
        return self._count_pifs

    @count_pifs.setter
    def count_pifs(self, count_pifs):
        self._count_pifs = count_pifs

    @count_pifs.deleter
    def count_pifs(self):
        self._count_pifs = None
