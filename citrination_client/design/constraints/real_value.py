from citrination_client.design.constraints.base import BaseConstraint

class RealValueConstraint(BaseConstraint):
    """
    Constrains a real valued column to a single value.
    """

    def __init__(self, descriptor, value=None):
        """
        Constructor.

        :param descriptor: The name of the column in the data
            view to which this constraint should be applied
        :type descriptor: str
        :param value: The value the column should be constrained to
        :type value: float
        """
        self._type = "real"        
        self._descriptor = descriptor
        self._value = value

    def options(self):
        return {
            "value": self._value
        }