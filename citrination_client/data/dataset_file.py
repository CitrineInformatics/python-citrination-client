class DatasetFile(object):
    """
    Class representation of a file in a dataset on Citrination.
    """

    def __init__(self, path, url=None):
        """
        Constructor.

        :param path: The files path
        :type path: str
        :param url: If present, a download URL for the file
        :type url: str
        """
        self._path = path
        self._url = url

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @path.deleter
    def path(self):
        self._path = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @url.deleter
    def url(self):
        self._url = None