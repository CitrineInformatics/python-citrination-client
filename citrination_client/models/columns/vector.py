from citrination_client.models.columns.base import BaseColumn
from citrination_client.base.errors import CitrinationClientError

class VectorColumn(BaseColumn):
    """
    An vector column configuration for a data view.
    Parameterized with the basic column options and a length parameter expressing the length of vectors in this column.
    """

    TYPE = "Vector"

    def __init__(self, name, role, group_by_key=False, units=None, length=None):
        """
        Constructor.

        :param name: The name of the column
        :type name: str
        :param role: The role the column will play in machine learning:
                       "Input"
                       "Output"
                       "Latent Variable"
                       "Ignore"
        :type role: str
        :param group_by_key: Whether or not this column should be used for
            grouping during cross validation
        :type group_by_key: bool
        :param units: Optionally, the units for this column
        :type units: str
        :param length: The length of vectors in this column
        :type length: int
        """
        super(VectorColumn, self).__init__(name=name,
                                           role=role,
                                           group_by_key=group_by_key,
                                           units=units)
        self.length = length

    def build_options(self):
        return {
            "length": self.length
        }

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        try:
            self._length = int(value)
        except ValueError:
            raise CitrinationClientError("When constructing a VectorColumn, parameter length must be castable as an int")

    @length.deleter
    def length(self):
        self._length = None
