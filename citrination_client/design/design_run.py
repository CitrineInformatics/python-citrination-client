class DesignRun(object):

    def __init__(self, uuid):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @uuid.deleter
    def uuid(self):
        self._uuid = None