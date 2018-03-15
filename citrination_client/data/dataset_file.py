class DatasetFile(object):

    def __init__(self, path, url=None):
        self._path = path
        self._url = url

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url