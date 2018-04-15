from citrination_client.design.constraints.base import BaseConstraint

class CategoricalConstraint(BaseConstraint):
    """
    Constrains a column to a particular set of categorical
    values.
    """

    def __init__(self, descriptor, categories):
        """
        Constructor.

        :param descriptor: The name of the column in the data
            view to which this constraint should be applied
        :type descriptor: str
        :param elements: An array of categories to constrain the descriptor to
        :type elements: list of str
        """
        self._type = "categorical"
        self._descriptor = descriptor
        self._categories = categories

    def options(self):
        return {
            "categories": self._categories,
        }