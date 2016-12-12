from six import string_types
from pypif import pif
from pypif.obj.common.pio import Pio
from pypif.util.serializable import Serializable


class PifSearchHit(Serializable):
    """
    Class to store a single PIF search hit.
    """

    def __init__(self, id=None, dataset=None, dataset_version=None, score=None, system=None, extracted=None):
        """
        Constructor.

        :param id: String with the ID of the record.
        :param dataset: Integer with the dataset of the record.
        :param dataset_version: Integer with the dataset version of the record.
        :param score: Score with the relevancy of the result.
        :param system: Pif System object that matched.
        :param extracted: Dictionary with a map of extracted property names to values.
        """
        self._id = None
        self.id = id
        self._dataset = None
        self.dataset = dataset
        self._dataset_version = None
        self.dataset_version = dataset_version
        self._score = None
        self.score = score
        self._system = None
        self.system = system
        self._extracted = None
        self.extracted = extracted

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @id.deleter
    def id(self):
        self._id = None

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        self._dataset = dataset

    @dataset.deleter
    def dataset(self):
        self._dataset = None

    @property
    def dataset_version(self):
        return self._dataset_version

    @dataset_version.setter
    def dataset_version(self, dataset_version):
        self._dataset_version = dataset_version

    @dataset_version.deleter
    def dataset_version(self):
        self._dataset_version = None

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @score.deleter
    def score(self):
        self._score = None

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        if system is None:
            self._system = None
        elif isinstance(system, string_types):
            self._system = pif.loads(system)
        elif isinstance(system, dict):
            self._system = pif.loado(system)
        elif isinstance(system, Pio):
            self._system = system
        else:
            raise TypeError('Not a valid system type: must be string, dict, or Pio, but got ' + str(type(system)))

    @system.deleter
    def system(self):
        self._system = None

    @property
    def extracted(self):
        return self._extracted

    @extracted.setter
    def extracted(self, extracted):
        self._extracted = extracted

    @extracted.deleter
    def extracted(self):
        self._extracted = None
