from pypif.util.serializable import Serializable


class BaseSearchResult(Serializable):
    """
    Base class for all search results.
    """

    def __init__(self, took=None, total_num_hits=None, max_score=None, hits=None, **kwargs):
        """
        Constructor.

        :param took: Number of milliseconds that the query took to execute.
        :param total_num_hits: Total number of hits.
        :param max_score: The maximum score.
        :param hits: List of hits.
        """
        self._took = None
        self.took = took
        self._total_num_hits = None
        self.total_num_hits = total_num_hits
        self._max_score = None
        self.max_score = max_score
        self._hits = None
        self.hits = hits

    @property
    def took(self):
        return self._took

    @took.setter
    def took(self, took):
        self._took = took

    @took.deleter
    def took(self):
        self._took = None

    @property
    def total_num_hits(self):
        return self._total_num_hits

    @total_num_hits.setter
    def total_num_hits(self, total_num_hits):
        self._total_num_hits = total_num_hits

    @total_num_hits.deleter
    def total_num_hits(self):
        self._total_num_hits = None

    @property
    def max_score(self):
        return self._max_score

    @max_score.setter
    def max_score(self, max_score):
        self._max_score = max_score

    @max_score.deleter
    def max_score(self):
        self._max_score = None

    @property
    def hits(self):
        return self._hits

    @hits.setter
    def hits(self, hits):
        self._hits = hits

    @hits.deleter
    def hits(self):
        self._hits = None
