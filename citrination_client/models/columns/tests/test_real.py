import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import *

class TestRealColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Band gap"
        self.role = "Input"
        self.group_by_key = False
        self.units = "eV"

    def test_real_column_validates_floatable(self):
        """
        Tests that the bounds options passed into the
        RealColumn constructor are validated as castable to float
        """

        # Non floatable lower
        lower_bound = "asdf"
        upper_bound = 1

        with pytest.raises(CitrinationClientError):
            RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Non floatable upper
        lower_bound = 0
        upper_bound = "asdf"

        with pytest.raises(CitrinationClientError):
            RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Some valid values; should not raise exceptions
        lower_bound = 0
        upper_bound = 10
        RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        lower_bound = "-Infinity"
        upper_bound = "Infinity"
        RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

    def test_real_column_validates_bounded_range(self):
        """
        Tests that the upper bound must be greater than the lower bound
        on RealColumn construction
        """

        # Invalid range, lower is greater than upper
        lower_bound = 10
        upper_bound = 1
        with pytest.raises(CitrinationClientError):
            RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

        # Valid range, lower is equal to upper
        lower_bound = 10
        upper_bound = 10
        RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, lower_bound=lower_bound, upper_bound=upper_bound)

    def test_real_column_serializes_correctly(self):
        """
        Tests that the RealColumn correctly expresses its options in
        dictionary format; particularly, that it stringifies Infinities
        for the back end
        """

        # Invalid range, lower is greater than upper
        lower_bound = float("-inf")
        upper_bound = float("inf")
        column = RealColumn(name=self.name, role=self.role, group_by_key=self.group_by_key, units=self.units, lower_bound=lower_bound, upper_bound=upper_bound)

        c_dict = column.to_dict()

        assert c_dict["name"]                   == self.name
        assert c_dict["role"]                   == self.role
        assert c_dict["group_by_key"]           == self.group_by_key
        assert c_dict["units"]                  == self.units
        assert c_dict["type"]                   == RealColumn.TYPE
        assert c_dict["options"]["lower_bound"] == "-Infinity"
        assert c_dict["options"]["upper_bound"] == "Infinity"