class DatasetVersion(object):
    """
    Class representation of a version of a dataset on Citrination.
    """

    def __init__(self, number):
        """
        Constructor.

        :param number: The number of the dataset version
        :type number: ints
        """
        self._number = number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @number.deleter
    def number(self):
        self._number = None