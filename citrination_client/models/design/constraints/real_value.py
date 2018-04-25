from citrination_client.models.design.constraints.base import BaseConstraint

class RealValueConstraint(BaseConstraint):
    """
    Constrains a real valued column to a single value.
    """

    def __init__(self, name, value=None):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param value: The value the column should be constrained to
        :type value: float
        """
        self._type = "real"        
        self._name = name
        self._value = value

    def options(self):
        return {
            "value": self._value
        }