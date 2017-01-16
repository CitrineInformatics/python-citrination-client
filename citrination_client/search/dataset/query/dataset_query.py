from pypif.util.serializable import Serializable
from citrination_client.search.pif.query.core.system_query import SystemQuery


class DatasetQuery(Serializable):
    """
    Class to store information about a dataset query.
    """

    def __init__(self, from_index=None, size=None, score_relevance=None, system=None, **kwargs):
        """
        Constructor.

        :param from_index: Integer with the first index of the record to return.
        :param size: Integer with the number of records to return.
        :param score_relevance: True/False to set whether relevance scores should be used.
        :param system: One or more :class:`SystemQuery` objects with the query to run.
        :param kwargs: Any other arguments. The only supported key is "from".
        """
        if 'from' in 'kwargs':
            self.from_index = kwargs['from']
        self._from = None
        self.from_index = from_index
        self._size = None
        self.size = size
        self._score_relevance = None
        self.score_relevance = score_relevance
        self._system = None
        self.system = system

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
    def score_relevance(self):
        return self._score_relevance

    @score_relevance.setter
    def score_relevance(self, score_relevance):
        self._score_relevance = score_relevance

    @score_relevance.deleter
    def score_relevance(self):
        self._score_relevance = None

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        self._system = self._get_object(SystemQuery, system)

    @system.deleter
    def system(self):
        self._system = None
