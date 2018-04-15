from citrination_client.design.constraints.base import BaseConstraint

class ElementalCompositionConstraint(BaseConstraint):
    """
    Constrains a composition or inorganic formula column
    to a particular percentage.
    """

    def __init__(self, descriptor, elements, minimum, maximum):
        """
        Constructor.

        :param descriptor: The name of the column in the data
            view to which this constraint should be applied
        :type descriptor: str
        :param elements: An array of element abbreviations as
            strings, e.g. ["Mg", "C"]
        :type elements: list of str
        :param minimum: The minimum value (< 100) as a percentage
            at which the specified elements should appear in
            candidate compositions
        :type minimum: float
        :param maximum: The maximum value (< 100) as a percentage
            at which the specified elements should appear in
            candidate compositions
        :type maximum: float
        """
        self._type = "elementalCompositionConstraint"
        self._elements = elements
        self._descriptor = descriptor
        self._min = minimum
        self._max = maximum

    def options(self):
        return {
            "elements": self._elements,
            "min": self._min,
            "max": self._max
        }