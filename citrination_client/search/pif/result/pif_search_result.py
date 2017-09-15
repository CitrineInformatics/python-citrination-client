from citrination_client.search.core.result.base_search_result import BaseSearchResult
from citrination_client.search.pif.result.pif_search_hit import PifSearchHit


class PifSearchResult(BaseSearchResult):
    """
    Class to store the results of a PIF query.
    """

    def __init__(self, took=None, total_num_hits=None, max_score=None, hits=None, **kwargs):
        """
        Constructor.

        :param took: Number of milliseconds that the query took to execute.
        :param total_num_hits: Total number of hits.
        :param max_score: The maximum score.
        :param hits: List of :class:`PifSearchHit` objects.
        """
        super(PifSearchResult, self).__init__(
            took=took, total_num_hits=total_num_hits, max_score=max_score,
            hits=self._get_object(PifSearchHit, hits), **kwargs)
