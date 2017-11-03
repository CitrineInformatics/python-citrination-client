from pypif.util.serializable import Serializable


class FileSearchHit(Serializable):
    """
    Class to store a single file search hit.
    """

    def __init__(self, dataset_id=None, dataset_version=None, id=None, score=None, name=None, updated_at=None, 
                 highlights=None, **kwargs):
        """
        Constructor.

        :param dataset_id: String with the ID of the dataset.
        :param dataset_version: Long with the version of the dataset.
        :param id: String with the ID of the record.
        :param score: Score with the relevancy of the result.
        :param name: Name of the dataset.
        :param updated_at: String with the last time that the dataset was updated.
        :param highlights: List of strings with the highlighted results.
        """
        self._dataset_id = None
        self.dataset_id = dataset_id
        self._dataset_version = None
        self.dataset_version = dataset_version
        self._id = None
        self.id = id
        self._score = None
        self.score = score
        self._name = None
        self.name = name
        self._updated_at = None
        self.updated_at = updated_at
        self._highlights = None
        self.highlights = highlights

    @property
    def dataset_id(self):
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        self._dataset_id = dataset_id

    @dataset_id.deleter
    def dataset_id(self):
        self._dataset_id = None

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
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        self._name = None

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = updated_at

    @updated_at.deleter
    def updated_at(self):
        self._updated_at = None

    @property
    def highlights(self):
        return self._highlights

    @highlights.setter
    def highlights(self, highlights):
        self._highlights = highlights

    @highlights.deleter
    def highlights(self):
        self._highlights = None
