from citrination_client.models.columns.base import BaseColumn
from citrination_client.base.errors import CitrinationClientError

class IntColumn(BaseColumn):
    """
    A integer column configuration for a data view. Parameterized
    with the basic column options and an upper and lower bound on the
    acceptable values for the column
    """

    TYPE = "Integer"

    def __init__(self, name, role, group_by_key=False, units=None, lower_bound=None, upper_bound=None):
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
        :param lower_bound: The lower bound for valid values for this column
        :type lower_bound: int
        :param upper_bound: The upper bound for valid values for this column
        :type upper_bound: int
        """
        super(IntColumn, self).__init__(name=name,
                                        role=role,
                                        group_by_key=group_by_key,
                                        units=units)
        # Default bounds to None to enable validation via the setter methods
        self._lower_bound = None
        self._upper_bound = None

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def build_options(self):
        return {
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound
        }

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value):
        self._lower_bound = self._cast_and_validate_int(value, "lower_bound")
        self._validate_bounds()

    @lower_bound.deleter
    def lower_bound(self):
        self._lower_bound = None

    @property
    def upper_bound(self):
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value):
        self._upper_bound = self._cast_and_validate_int(value, "upper_bound")
        self._validate_bounds()

    @upper_bound.deleter
    def upper_bound(self):
        self._upper_bound = None

    def _both_bounds_present(self):
        return self.lower_bound is not None and self.upper_bound is not None

    def _validate_bounds(self):
        if self._both_bounds_present() and self._lower_bound > self._upper_bound:
            raise CitrinationClientError("When constructing a IntColumn, lower_bound must be less than upper_bound")

    def _cast_and_validate_int(self, value, attr_name):
        try:
            return int(value)
        except ValueError:
            raise CitrinationClientError("For a IntColumn, {} must be castable as an integer".format(attr_name))
