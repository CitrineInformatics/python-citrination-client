from pypif.util.serializable import Serializable


class UnitsNormalization(Serializable):
    """
    Configuration for normalization of units.
    """

    def __init__(self, search=None, extract=None):
        """
        Constructor.

        :param search: String with the units to run the query against.
        :param extract: String with the units to normalize results to.
        """
        self._search = None
        self.search = search
        self._extract = None
        self.extract = extract

    @property
    def search(self):
        return self._search

    @search.setter
    def search(self, search):
        self._search = search

    @search.deleter
    def search(self):
        self._search = None

    @property
    def extract(self):
        return self._extract

    @extract.setter
    def extract(self, extract):
        self._extract = extract

    @extract.deleter
    def extract(self):
        self._extract = None
