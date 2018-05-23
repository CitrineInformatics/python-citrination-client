from citrination_client.models.columns.base import BaseColumn
from citrination_client.base.errors import CitrinationClientError

from six import string_types

class CategoricalColumn(BaseColumn):
    """
    A categorical column configuration for a data view. Parameterized
    with the basic column options and a list of valid values for the
    column to have.
    """

    TYPE = "Categorical"

    def __init__(self, name, role, group_by_key=False, units=None, categories=[]):
        """
        Constructor.

        :param name: The name of the column
        :type name: str
        :param role: The role the column will play in machine learning:
                       "Input"
                       "Output"
                       "Latent Variable"
                       "Ignore"
        :type role: str
        :param group_by_key: Whether or not this column should be used for
            grouping during cross validation
        :type group_by_key: bool
        :param units: Optionally, the units for the column
        :type units: str
        :param categories: An array of strings that are valid values for data
            in this column
        :type categories: list of str
        """
        super(CategoricalColumn, self).__init__(name=name,
                                                role=role,
                                                group_by_key=group_by_key,
                                                units=units)
        self.categories = categories

    def build_options(self):
        return {
            "categories": self.categories
        }

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._validate_categories(value)
        self._categories = [str(v) for v in value]

    @categories.deleter
    def categories(self):
        self._categories = None

    def _validate_categories(self, categories):
        if type(categories) is not list:
            raise CitrinationClientError("CategoricalColumn requires that the categories value is a list of strings")

        if not all(isinstance(item, string_types) for item in categories):
            raise CitrinationClientError("CategoricalColumn requires that the categories value is a list of strings")
