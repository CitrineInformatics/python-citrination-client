import pytest
from citrination_sdk_internal.data_views.columns import *
from citrination_client.errors import *

class TestVectorColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Band gap"
        self.role = "Input"
        self.group_by_key = False
        self.units = "eV"

    def test_vector_column_validates_length_castable_to_int(self):
        """
        Tests that the length option passed into the RealColumn constructor
        is castable to int
        """

        # Non intable length
        length = "asdf"

        with pytest.raises(CitrinationClientError):
            VectorColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, length=length)

    def test_vector_column_serializes_length_correctly(self):
        """
        Tests that the VectorColumn class expresses the length option correctly
        in its dictionary form.
        """

        length = 10.0

        column = VectorColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, units=self.units, length=length)

        c_dict = column.to_dict()

        assert c_dict["name"]                  == self.name
        assert c_dict["role"]                  == self.role
        assert c_dict["group_by_key"]          == self.group_by_key
        assert c_dict["units"]                 == self.units
        assert c_dict["type"]                  == VectorColumn.TYPE
        assert c_dict["options"]["length"]     == 10