from pypif.util.serializable import Serializable


class MultiQuery(Serializable):
    """
    Base class for all multi-search requests.
    """

    def __init__(self, queries=None, **kwargs):
        """
        Constructor.

        :param queries: One or more queries to run.
        """
        self._queries = None
        self.queries = queries

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, queries):
        self._queries = queries

    @queries.deleter
    def queries(self):
        self._queries = None
