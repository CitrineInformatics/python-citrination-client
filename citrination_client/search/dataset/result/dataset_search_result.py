from pypif.util.serializable import Serializable
from citrination_client.search.dataset.result.dataset_search_hit import DatasetSearchHit


class DatasetSearchResult(Serializable):
    """
    Class to store the results of a dataset query.
    """

    def __init__(self, took=None, total_num_hits=None, hits=None):
        """
        Constructor.

        :param took: Number of milliseconds that the query took to execute.
        :param total_num_hits: Total number of hits.
        :param hits: List of :class:`.DatasetSearchHit` objects.
        """
        self._took = None
        self.took = took
        self._total_num_hits = None
        self.total_num_hits = total_num_hits
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
    def hits(self):
        return self._hits

    @hits.setter
    def hits(self, hits):
        self._hits = self._get_object(DatasetSearchHit, hits)

    @hits.deleter
    def hits(self):
        self._hits = None
