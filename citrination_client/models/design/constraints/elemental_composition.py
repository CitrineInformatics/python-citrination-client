from citrination_client.models.design.constraints.base import BaseConstraint
from citrination_client.base.errors import CitrinationClientError

class ElementalCompositionConstraint(BaseConstraint):
    """
    Constrains a composition or inorganic formula column
    to a particular percentage.
    """

    def __init__(self, name, elements, minimum, maximum):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param elements: An array of element abbreviations as
            strings, e.g. ["Mg", "C"]
        :type elements: list of str
        :param minimum: The minimum value (<= 100) as a percentage
            at which the specified elements should appear in
            candidate compositions
        :type minimum: float
        :param maximum: The maximum value (<= 100) as a percentage
            at which the specified elements should appear in
            candidate compositions
        :type maximum: float
        """
        if not 0 <= minimum <= 100:
            raise CitrinationClientError("ElementalCompositionConstraint requires that minimum be between 0 and 100")

        if not 0 <= maximum <= 100:
            raise CitrinationClientError("ElementalCompositionConstraint requires that maximum be between 0 and 100")

        if not maximum >= minimum:
            raise CitrinationClientError("ElementalCompositionConstraint requires that maximum be greater than minimum")


        self._type = "elementalCompositionConstraint"
        self._elements = elements
        self._name = name
        self._min = minimum
        self._max = maximum

    def options(self):
        return {
            "elements": self._elements,
            "min": self._min,
            "max": self._max
        }