from citrination_client.design.constraints.base import BaseConstraint

class RealRangeConstraint(BaseConstraint):
    """
    Constrains a real valued column to a range.
    """

    def __init__(self, descriptor, minimum, maximum):
        """
        Constructor.

        :param descriptor: The name of the column in the data
            view to which this constraint should be applied
        :type descriptor: str
        :param minimum: The minimum allowed value
        :type minimum: float
        :param maximum: The maximum allowed value
        :type maximum: float
        """
        self._type = "real"        
        self._descriptor = descriptor
        self._min = minimum
        self._max = maximum

    def options(self):
        return {
            "min": self._min,
            "max": self._max
        }