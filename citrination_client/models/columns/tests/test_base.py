import pytest
from citrination_client.models.columns import *
from citrination_client.base.errors import *

class TestBaseColumn(object):

    @classmethod
    def setup_class(self):
        self.name = "Property Band gap"
        self.role = "Input"
        self.group_by_key = False
        self.units = "eV"

    def test_base_column_validates_role(self):
        try:
            column = BaseColumn(name=self.name, role="asdf")
            assert False, "Base column should validate role"
        except CitrinationClientError:
            pass
