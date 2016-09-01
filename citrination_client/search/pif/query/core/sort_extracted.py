from pypif.util.serializable import Serializable


class SortExtracted(Serializable):
    """
    Class with information about sorting on an extracted field.
    """

    def __init__(self, extract_as, sort):
        """
        Constructor.

        :param extract_as: String with the label of the extract value to sort on.
        :param sort: String equal to one of "ASCENDING" or "DESCENDING".
        """
        self._extract_as = None
        self.extract_as = extract_as
        self._sort = None
        self.sort = sort

    @property
    def extract_as(self):
        return self._extract_as

    @extract_as.setter
    def extract_as(self, extract_as):
        self._extract_as = extract_as

    @extract_as.deleter
    def extract_as(self):
        self._extract_as = None

    @property
    def sort(self):
        return self._sort

    @sort.setter
    def sort(self, sort):
        self._sort = sort

    @sort.deleter
    def sort(self):
        self._sort = None
