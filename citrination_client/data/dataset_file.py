class DatasetFile(object):
    """
    Class representation of a file in a dataset on Citrination.
    """

    def __init__(self, path, url=None):
        """
        Constructor.

        :param path: The files path
        :param url: If present, a download URL for the file
        """
        self._path = path
        self._url = url

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url