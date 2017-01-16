from pypif.util.serializable import Serializable


class DatasetSearchHit(Serializable):
    """
    Class to store a single dataset search hit.
    """

    def __init__(self, id=None, score=None):
        """
        Constructor.

        :param id: String with the ID of the record.
        :param score: Score with the relevancy of the result.
        """
        self._id = None
        self.id = id
        self._score = None
        self.score = score

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
