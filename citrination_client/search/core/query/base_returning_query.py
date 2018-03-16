from citrination_client.search.core.query.data_scope import DataScope


class BaseReturningQuery(DataScope):
    """
    Base class for all queries against datasets and the items that they contain on Citrination.
    """

    def __init__(self, query=None, extraction_sort=None, from_index=None, size=None, random_results=None,
                 random_seed=None, score_relevance=None, return_max_score=None, timeout=None, **kwargs):
        """
        Base class for all queries against datasets and the items that they contain on Citrination.

        :param query: One or more :class:`DataQuery` objects with the queries to run.
        :param extraction_sort: A single :class:`ExtractionSort` object for sorting.
        :param from_index: Index of the first hit that should be returned.
        :param size: Total number of hits the should be returned.
        :param random_results: Whether to return a random set of records.
        :param random_seed: The random seed to use.
        :param score_relevance: Whether to use relevance scoring.
        :param return_max_score: Whether to return the maximum score.
        :param timeout: The number of milliseconds to wait for the query to execute.
        """
        super(BaseReturningQuery, self).__init__(query=query, extraction_sort=extraction_sort, **kwargs)
        if 'from' in 'kwargs':
            self.from_index = kwargs['from']
        self._from = None
        self.from_index = from_index
        self._size = None
        self.size = size
        self._random_results = None
        self.random_results = random_results
        self._random_seed = None
        self.random_seed = random_seed
        self._score_relevance = None
        self.score_relevance = score_relevance
        self._return_max_score = None
        self.return_max_score = return_max_score
        self._timeout = None
        self.timeout = timeout

    @property
    def from_index(self):
        return self._from

    @from_index.setter
    def from_index(self, from_index):
        self._from = from_index

    @from_index.deleter
    def from_index(self):
        self._from = None

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @size.deleter
    def size(self):
        self._size = None

    @property
    def random_results(self):
        return self._random_results

    @random_results.setter
    def random_results(self, random_results):
        self._random_results = random_results

    @random_results.deleter
    def random_results(self):
        self._random_results = None

    @property
    def random_seed(self):
        return self._random_seed

    @random_seed.setter
    def random_seed(self, random_seed):
        self._random_seed = random_seed

    @random_seed.deleter
    def random_seed(self):
        self._random_seed = None

    @property
    def score_relevance(self):
        return self._score_relevance

    @score_relevance.setter
    def score_relevance(self, score_relevance):
        self._score_relevance = score_relevance

    @score_relevance.deleter
    def score_relevance(self):
        self._score_relevance = None

    @property
    def return_max_score(self):
        return self._return_max_score

    @return_max_score.setter
    def return_max_score(self, return_max_score):
        self._return_max_score = return_max_score

    @return_max_score.deleter
    def return_max_score(self):
        self._return_max_score = None

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout

    @timeout.deleter
    def timeout(self):
        self._timeout = None
