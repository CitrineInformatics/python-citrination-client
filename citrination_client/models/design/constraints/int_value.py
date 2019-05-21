from citrination_client.models.design.constraints.base import BaseConstraint


class IntValueConstraint(BaseConstraint):
    """
    Constrains a integer valued column to a single value.
    """

    def __init__(self, name, value=None):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param value: The value the column should be constrained to
        :type value: int
        """
        self._type = "integer"
        self._name = name
        self._value = value

    def options(self):
        return {
            "value": self._value
        }