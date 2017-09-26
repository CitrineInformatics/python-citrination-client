from pypif.util.serializable import Serializable


class ExtractionSort(Serializable):
    """
    Class to store information about a sort on an extracted field.
    """

    def __init__(self, key=None, order=None, **kwargs):
        """
        Constructor.

        :param key: String with the key that will be sorted on.
        :param order: The order to use. Either ASCENDING or DESCENDING.
        """
        self._key = None
        self.key = key
        self._order = None
        self.order = order

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @key.deleter
    def key(self):
        self._key = None

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    @order.deleter
    def order(self):
        self._order = None
