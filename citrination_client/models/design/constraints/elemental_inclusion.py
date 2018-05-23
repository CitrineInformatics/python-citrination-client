from citrination_client.models.design.constraints.base import BaseConstraint
from citrination_client.base.errors import CitrinationClientError

class ElementalInclusionConstraint(BaseConstraint):
    """
    Constraint class which allows the assertion that a set of 
    elements is included in the candidate compositions
    """

    def __init__(self, name, elements, logic):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param elements: An array of element abbreviations as
            strings, e.g. ["Mg", "C"]
        :type elements: list of str
        :param logic: The logic to apply to the constraint; either
            "must", "should", or "exclude"
        :type logic: str
        """
        bad_logic_msg = "ElementalInclusionConstraint must be initialized with the logic parameter equal to \"must\", \"should\", or \"exclude\""

        if logic not in ["must", "should", "exclude"]:
            raise CitrinationClientError(bad_logic_msg)

        self._name = name
        self._type = "elementalInclusionConstraint"
        self._elements = elements
        self._logic = logic

    def options(self):
        return {
            "elements": self._elements,
            "logic": self._logic
        }