import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import *

class TestIntColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Ingredient count"
        self.role = "Input"
        self.group_by_key = False
        self.units = "ingredients"

    def test_int_column_validates_intable(self):
        """
        Tests that the bounds options passed into the
        IntColumn constructor are validated as castable to int
        """

        # Non intable lower
        lower_bound = "asdf"
        upper_bound = 1

        with pytest.raises(CitrinationClientError):
            IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Non intable upper
        lower_bound = 0
        upper_bound = "asdf"

        with pytest.raises(CitrinationClientError):
            IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Some valid values; should not raise exceptions
        lower_bound = 0
        upper_bound = 10
        IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

    def test_int_column_validates_bounded_range(self):
        """
        Tests that the upper bound must be greater than the lower bound
        on IntColumn construction
        """

        # Invalid range, lower is greater than upper
        lower_bound = 10
        upper_bound = 1
        with pytest.raises(CitrinationClientError):
            IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Valid range, lower is equal to upper
        lower_bound = 10
        upper_bound = 10
        IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

    def test_int_column_serializes_correctly(self):
        """
        Tests that the IntColumn correctly expresses its options in
        dictionary format; particularly, that it stringifies Infinities
        for the back end
        """

        # Invalid range, lower is greater than upper
        lower_bound = 0
        upper_bound = 10
        column = IntColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, units=self.units, lower_bound=lower_bound, upper_bound=upper_bound)

        c_dict = column.to_dict()

        assert c_dict["name"]                   == self.name
        assert c_dict["role"]                   == self.role
        assert c_dict["group_by_key"]           == self.group_by_key
        assert c_dict["units"]                  == self.units
        assert c_dict["type"]                   == IntColumn.TYPE
        assert c_dict["options"]["lower_bound"] == lower_bound
        assert c_dict["options"]["upper_bound"] == upper_bound
