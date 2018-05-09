from pypif.util.serializable import Serializable

from citrination_client.search.dataset.query.dataset_query import DatasetQuery
from citrination_client.search.file.query.file_query import FileQuery
from citrination_client.search.pif.query.pif_system_query import PifSystemQuery


class DataQuery(Serializable):
    """
    Query against dataset metadata, PIF content, file content, or some combination of those types.
    """

    def __init__(self, logic=None, weight=None, simple=None, simple_weight=None, dataset=None, system=None, file=None,
                 query=None, **kwargs):
        """
        Constructor.

        :param logic: The logic to apply to the query ('SHOULD', 'MUST', 'MUST_NOT', or 'OPTIONAL').
        :param weight: Weight for the query.
        :param simple: String with the simple search to run against all fields.
        :param simple_weight: Dictionary of relative paths to their weights for simple queries.
        :param dataset: One or more :class:`DatasetQuery` objects with queries against dataset metadata.
        :param system: One or more :class:`PifSystemQuery` objects with queries against PIF systems
        :param file: One or more :class:`FileQuery` objects with queries against file content or metadata.
        :type file: :class:`FileQuery`
        :param query: Nested list of :class:`DataQuery` objects.
        """
        self._logic = None
        self.logic = logic
        self._weight = None
        self.weight = weight
        self._simple = None
        self.simple = simple
        self._simple_weight = None
        self.simple_weight = simple_weight
        self._dataset = None
        self.dataset = dataset
        self._system = None
        self.system = system
        self._file = None
        self.file = file
        self._query = None
        self.query = query

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, logic):
        self._logic = logic

    @logic.deleter
    def logic(self):
        self._logic = None

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @weight.deleter
    def weight(self):
        self._weight = None

    @property
    def simple(self):
        return self._simple

    @simple.setter
    def simple(self, simple):
        self._simple = simple

    @simple.deleter
    def simple(self):
        self._simple = None

    @property
    def simple_weight(self):
        return self._simple_weight

    @simple_weight.setter
    def simple_weight(self, simple_weight):
        self._simple_weight = simple_weight

    @simple_weight.deleter
    def simple_weight(self):
        self._simple_weight = None

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        self._dataset = self._get_object(DatasetQuery, dataset)

    @dataset.deleter
    def dataset(self):
        self._dataset = None

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        self._system = self._get_object(PifSystemQuery, system)

    @system.deleter
    def system(self):
        self._system = None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = self._get_object(FileQuery, file)

    @file.deleter
    def file(self):
        self._file = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = self._get_object(DataQuery, query)

    @query.deleter
    def query(self):
        self._query = None
