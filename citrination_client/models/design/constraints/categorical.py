from citrination_client.models.design.constraints.base import BaseConstraint

class CategoricalConstraint(BaseConstraint):
    """
    Constrains a column to a particular set of categorical
    values.
    """

    def __init__(self, name, accepted_categories):
        """
        Constructor.

        :param name: The name of the column in the data
            view to which this constraint should be applied
        :type name: str
        :param accepted_categories: An array of categories to constrain the name to
        :type accepted_categories: list of str
        """
        self._type = "categorical"
        self._name = name
        self._categories = accepted_categories

    def options(self):
        return {
            "categories": self._categories,
        }