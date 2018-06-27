from citrination_client.models.design.constraints.base import BaseConstraint
from citrination_client.base.errors import CitrinationClientError
import citrination_client.util.maths as maths

class RealRangeConstraint(BaseConstraint):
    """
    Constrains a real valued column to a range.
    """

    def __init__(self, name, minimum, maximum):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param minimum: The minimum allowed value
        :type minimum: float
        :param maximum: The maximum allowed value
        :type maximum: float
        """

        try:
            minimum_f = float(minimum)
            maximum_f = float(maximum)
        except TypeError:
            raise CitrinationClientError("RealRangeConstraint requires that minimum and maximum must be able to be cast to float")

        if minimum_f > maximum_f:
            raise CitrinationClientError("RealRangeConstraint requires that minimum be less than maximum")

        self._min = minimum_f
        self._max = maximum_f
        self._type = "real"
        self._name = name

    def options(self):
        minimum = maths.convert_infinity_to_string(self._min)
        maximum = maths.convert_infinity_to_string(self._max)

        return {
            "min": minimum,
            "max": maximum
        }