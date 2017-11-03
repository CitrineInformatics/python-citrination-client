from pypif.util.serializable import Serializable


class DatasetSearchHit(Serializable):
    """
    Class to store a single dataset search hit.
    """

    def __init__(self, id=None, score=None, is_featured=None, name=None, description=None, owner=None, email=None, 
                 num_pifs=None, updated_at=None, **kwargs):
        """
        Constructor.

        :param id: String with the ID of the record.
        :param score: Score with the relevancy of the result.
        :param is_featured: Whether the dataset is a featured one.
        :param name: Name of the dataset.
        :param description: Description of the dataset.
        :param owner: Name of the owner of the dataset.
        :param email: Email address of the owner of the dataset.
        :param num_pifs: Number of PIFs in the dataset.
        :param updated_at: String with the last time that the dataset was updated.
        """
        self._id = None
        self.id = id
        self._score = None
        self.score = score
        self._is_featured = None
        self.is_featured = is_featured
        self._name = None
        self.name = name
        self._description = None
        self.description = description
        self._owner = None
        self.owner = owner
        self._email = None
        self.email = email
        self._num_pifs = None
        self.num_pifs = num_pifs
        self._updated_at = None
        self.updated_at = updated_at

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
    def is_featured(self):
        return self._is_featured

    @is_featured.setter
    def is_featured(self, is_featured):
        self._is_featured = is_featured

    @is_featured.deleter
    def is_featured(self):
        self._is_featured = None

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
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @description.deleter
    def description(self):
        self._description = None

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    @owner.deleter
    def owner(self):
        self._owner = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @email.deleter
    def email(self):
        self._email = None

    @property
    def num_pifs(self):
        return self._num_pifs

    @num_pifs.setter
    def num_pifs(self, num_pifs):
        self._num_pifs = num_pifs

    @num_pifs.deleter
    def num_pifs(self):
        self._num_pifs = None

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = updated_at

    @updated_at.deleter
    def updated_at(self):
        self._updated_at = None
