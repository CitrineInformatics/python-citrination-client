from pypif.util.serializable import Serializable
from citrination_client.search.pif.query.core.sort_extracted import SortExtracted
from citrination_client.search.pif.query.core.system_query import SystemQuery


class PifQuery(Serializable):
    """
    Class to store information about a PIF query.
    """

    def __init__(self, from_index=None, size=None, return_system=None, add_latex=None,
                 score_relevance=None, sort_extracted=None, system=None, **kwargs):
        """
        Constructor.

        :param from_index: Integer with the first index of the record to return.
        :param size: Integer with the number of records to return.
        :param return_system: True/False to set whether PIF systems will be returned.
        :param add_latex: True/False to set whether latex will be injected into results.
        :param score_relevance: True/False to set whether relevance scores should be used.
        :param sort_extracted: One or more :class:`SortedExtracted` objects with sorts to apply.
        :param system: A single :class:`SystemQuery` object with the query to run.
        :param kwargs: Any other arguments. The only supported key is "from".
        """
        if 'from' in 'kwargs':
            self.from_index = kwargs['from']
        self._from = None
        self.from_index = from_index
        self._size = None
        self.size = size
        self._return_system = None
        self.return_system = return_system
        self._add_latex = None
        self.add_latex = add_latex
        self._score_relevance = None
        self.score_relevance = score_relevance
        self._sort_extracted = None
        self.sort_extracted = sort_extracted
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
    def return_system(self):
        return self._return_system

    @return_system.setter
    def return_system(self, return_system):
        self._return_system = return_system

    @return_system.deleter
    def return_system(self):
        self._return_system = None

    @property
    def add_latex(self):
        return self._add_latex

    @add_latex.setter
    def add_latex(self, add_latex):
        self._add_latex = add_latex

    @add_latex.deleter
    def add_latex(self):
        self._add_latex = None

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
    def sort_extracted(self):
        return self._sort_extracted

    @sort_extracted.setter
    def sort_extracted(self, sort_extracted):
        self._sort_extracted = self._get_object(SortExtracted, sort_extracted)

    @sort_extracted.deleter
    def sort_extracted(self):
        self._sort_extracted = None

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        self._system = self._get_object(SystemQuery, system)

    @system.deleter
    def system(self):
        self._system = None
