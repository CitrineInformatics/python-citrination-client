from citrination_client.models.design.constraints.base import BaseConstraint
from citrination_client.base.errors import CitrinationClientError
import citrination_client.util.maths as maths


class IntRangeConstraint(BaseConstraint):
    """
    Constrains an integer valued column to a range.
    """

    def __init__(self, name, minimum, maximum):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param minimum: The minimum allowed value
        :type minimum: int
        :param maximum: The maximum allowed value
        :type maximum: int
        """

        try:
            minimum_int = int(minimum)
            maximum_int = int(maximum)
        except TypeError:
            raise CitrinationClientError("IntRangeConstraint requires that minimum and maximum must be able to be cast to an integer")

        if minimum_int > maximum_int:
            raise CitrinationClientError("IntRangeConstraint requires that minimum be less than maximum")

        self._min = minimum_int
        self._max = maximum_int
        self._type = "integer"
        self._name = name

    def options(self):
        minimum = maths.convert_infinity_to_string(self._min)
        maximum = maths.convert_infinity_to_string(self._max)

        return {
            "min": minimum,
            "max": maximum
        }