from pypif.util.serializable import Serializable
from citrination_client.search.pif.query.core.system_query import SystemQuery


class DatasetQuery(Serializable):
    """
    Class to store information about a dataset query.
    """

    def __init__(self, from_index=None, size=None, random_results=None, random_seed=None, score_relevance=None,
                 count_pifs=None, system=None, **kwargs):
        """
        Constructor.

        :param from_index: Integer with the first index of the record to return.
        :param size: Integer with the number of records to return.
        :param random_results: True/False to set whether random results are returned.
        :param random_seed: Integer to set the seed for generating random results.
        :param score_relevance: True/False to set whether relevance scores should be used.
        :param count_pifs: True/False to set whether to count the number of PIFs in each dataset.
        :param system: One or more :class:`SystemQuery` objects with the query to run.
        :param kwargs: Any other arguments. The only supported key is "from".
        """
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
        self._count_pifs = None
        self.count_pifs = count_pifs
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
    def count_pifs(self):
        return self._count_pifs

    @count_pifs.setter
    def count_pifs(self, count_pifs):
        self._count_pifs = count_pifs

    @count_pifs.deleter
    def count_pifs(self):
        self._count_pifs = None

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        self._system = self._get_object(SystemQuery, system)

    @system.deleter
    def system(self):
        self._system = None
