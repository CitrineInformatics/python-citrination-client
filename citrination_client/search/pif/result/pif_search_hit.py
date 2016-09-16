from six import string_types
from pypif import pif
from pypif.obj.common.pio import Pio
from pypif.util.serializable import Serializable


class PifSearchHit(Serializable):
    """
    Class to store a single PIF search hit.
    """

    def __init__(self, id=None, system=None, extracted=None):
        """
        Constructor.

        :param id: String with the ID of the record.
        :param system: Pif System object that matched.
        :param extracted: Dictionary with a map of extracted property names to values.
        """
        self._id = None
        self.id = id
        self._system = None
        self.system = system
        self._extracted = None
        self.extracted = extracted

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
    def system(self):
        return self._system

    @system.setter
    def system(self, system):
        if isinstance(system, string_types):
            self._system = pif.loads(system)
        elif isinstance(system, dict):
            self._system = pif.loado(system)
        elif isinstance(system, Pio):
            self._system = system
        else:
            raise TypeError('Not a valid system type: must be string, dict, or Pio, but got ' + str(type(system)))

    @system.deleter
    def system(self):
        self._system = None

    @property
    def extracted(self):
        return self._extracted

    @extracted.setter
    def extracted(self, extracted):
        self._extracted = extracted

    @extracted.deleter
    def extracted(self):
        self._extracted = None
