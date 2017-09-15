from pypif.util.serializable import Serializable

from citrination_client.search.pif.result.pif_multi_search_result_element import PifMultiSearchResultElement


class PifMultiSearchResult(Serializable):
    """
    Class to store the results of a PIF multi-query.
    """

    def __init__(self, took=None, results=None, **kwargs):
        """
        Constructor.

        :param took: Number of milliseconds that the query took to execute.
        :param results: List of :class:`PifMultiSearchResultElement` objects.
        """
        self._took = None
        self.took = took
        self._results = None
        self.results = results

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
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = self._get_object(PifMultiSearchResultElement, results)

    @results.deleter
    def results(self):
        self._results = None
