import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import *

class TestCategoricalColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Band gap"
        self.role = "Input"
        self.group_by_key = False
        self.units = "eV"

    def test_categorical_column_writes_categories_correctly(self):
        categories = ["Grey", "Blue"]

        column = CategoricalColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, categories=categories)

        c_dict = column.to_dict()

        assert c_dict["name"]                  == self.name
        assert c_dict["role"]                  == self.role
        assert c_dict["group_by_key"]          == self.group_by_key
        assert c_dict["type"]                  == CategoricalColumn.TYPE
        assert c_dict["units"]                 == None
        assert c_dict["options"]["categories"] == categories

    def test_categorical_column_validates_categories(self):
        """
        Tests that the CategoricalColumn class validates that the categories
        value is a list of strings.
        """

        categories = 1

        with pytest.raises(CitrinationClientError):
            CategoricalColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, categories=categories)

        categories = ["Grey", 1]
        with pytest.raises(CitrinationClientError):
            CategoricalColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, categories=categories)

        categories = ["Grey", "Blue"]
        CategoricalColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, categories=categories)
