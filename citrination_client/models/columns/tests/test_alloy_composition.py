import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import CitrinationClientError

class TestAlloyCompositionColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Band gap"
        self.role = "Input"
        self.group_by_key = False
        self.units = "eV"

    def test_alloy_composition_column_serializes_options_correctly(self):
        """
        Tests that the AlloyCompositionColumn correctly expresses it's
        configuration (balance_element, basis, threshold) in its options
        dictionary
        """

        basis = 200.0
        balance_element = "ALUMINUM"

        column = AlloyCompositionColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, units=self.units, basis=basis, balance_element=balance_element)

        c_dict = column.to_dict()

        assert c_dict["name"]                       == self.name
        assert c_dict["role"]                       == self.role
        assert c_dict["group_by_key"]               == self.group_by_key
        assert c_dict["units"]                      == self.units
        assert c_dict["type"]                       == AlloyCompositionColumn.TYPE
        assert c_dict["options"]["basis"]           == basis
        assert c_dict["options"]["balance_element"] == balance_element
