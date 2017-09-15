from pypif.util.serializable import Serializable

from citrination_client.search.pif.result.pif_search_result import PifSearchResult


class PifMultiSearchResultElement(Serializable):
    """
    A single search result as a part of a pif multi-query.
    """
    
    def __init__(self, result=None, status=None, **kwargs):
        """
        Constructor.
        
        :param result: A single :class:`PifSearchResult` object with the query results.
        :param status: 'SUCCESS', 'ERROR', or 'NOT_EXECUTED'.
        """
        self._result = None
        self.result = result
        self._status = None
        self.status = status

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = self._get_object(PifSearchResult, result)

    @result.deleter
    def result(self):
        self._result = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @status.deleter
    def status(self):
        self._status = None
