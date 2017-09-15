from citrination_client.search.core.result.base_search_result import BaseSearchResult
from citrination_client.search.dataset.result.dataset_search_hit import DatasetSearchHit


class DatasetSearchResult(BaseSearchResult):
    """
    Class to store the results of a dataset query.
    """

    def __init__(self, took=None, total_num_hits=None, max_score=None, hits=None, **kwargs):
        """
        Constructor.

        :param took: Number of milliseconds that the query took to execute.
        :param total_num_hits: Total number of hits.
        :param max_score: The maximum score.
        :param hits: List of :class:`DatasetSearchHit` objects.
        """
        super(DatasetSearchResult, self).__init__(
            took=took, total_num_hits=total_num_hits, max_score=max_score,
            hits=self._get_object(DatasetSearchHit, hits), **kwargs)
