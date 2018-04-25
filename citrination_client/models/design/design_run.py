class DesignRun(object):
    """
    An in progress design run. Contains a UUID which is the identifier
    for the run.
    """

    def __init__(self, uuid):
        """
        Constructor.

        :param uuid: The UUID of an in progress design run.
        :type uuid: str
        """
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