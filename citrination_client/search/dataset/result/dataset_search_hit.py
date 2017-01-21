from pypif.util.serializable import Serializable


class DatasetSearchHit(Serializable):
    """
    Class to store a single dataset search hit.
    """

    def __init__(self, id=None, score=None, num_pifs=None):
        """
        Constructor.

        :param id: String with the ID of the record.
        :param score: Score with the relevancy of the result.
        :param num_pifs: Number of PIFs in the dataset.
        """
        self._id = None
        self.id = id
        self._score = None
        self.score = score
        self._num_pifs = None
        self.num_pifs = num_pifs

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
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @score.deleter
    def score(self):
        self._score = None

    @property
    def num_pifs(self):
        return self._num_pifs

    @num_pifs.setter
    def num_pifs(self, num_pifs):
        self._num_pifs = num_pifs

    @num_pifs.deleter
    def num_pifs(self):
        self._num_pifs = None
