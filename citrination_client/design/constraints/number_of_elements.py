from citrination_client.design.constraints.base import BaseConstraint

class NumberOfElementsConstraint(BaseConstraint):
    """
    A constraint which, when applied, limits the number of elements
    in the candidates' compositions.
    """

    def __init__(self, descriptor, minimum, maximum):
        """
        Constructor.

        :param descriptor: The name of the column in the data
            view to which this constraint should be applied
        :type descriptor: str
        :param min: The minimum number of elements in the composition
        :type min: int
        :param max: The maximum number of elements in the composition
        :type max: int
        """
        self._type = "numberOfElementsConstraint"
        self._descriptor = descriptor
        self._min = minimum
        self._max = maximum

    def options(self):
        return {
            "min": self._min,
            "max": self._max
        }