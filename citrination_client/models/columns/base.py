from citrination_client.base.errors import CitrinationClientError

class BaseColumn(object):
    """
    Base class for column configuration in a data view. Subclasses
    each represent one type of column.
    """

    def __init__(self, name, role, group_by_key=False, units=None):
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
        """
        self._name = name
        self._units = units
        self.role = role
        self._type = self.__class__.TYPE
        self._group_by_key = group_by_key

    def to_dict(self):
        """
        Converts the column to a dictionary representation accepted
        by the Citrination server.

        :return: Dictionary with basic options, plus any column type specific
            options held under the "options" key
        :rtype: dict
        """
        return {
            "type": self.type,
            "name": self.name,
            "group_by_key": self.group_by_key,
            "role": self.role,
            "units": self.units,
            "options": self.build_options()
        }

    def build_options(self):
        """
        Default value for optional column configuration. Only child
        classes will have non-None values for this field. Value
        depends on child class implementation.

        Note: Some child classes do not require any extra options
        (e.g. OrganicChemicalFormula), in that case, this implementation
        will be invoked and no options will be present in the dictionary.

        :return: Options dictionary, or None if not implemented in child
        :rtype: dict or None
        """
        return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        self._name = None

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._validate_role(value)
        self._role = value

    @role.deleter
    def role(self):
        self._role = None

    @property
    def group_by_key(self):
        return self._group_by_key

    @group_by_key.setter
    def group_by_key(self, value):
        self._group_by_key = value

    @group_by_key.deleter
    def group_by_key(self):
        self._group_by_key = None

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    @units.deleter
    def units(self):
        self._units = None

    @property
    def type(self):
        """
        Returns the type of the column. This value is
        read only because the valid value is defined by the
        column type and is set internally.
        """
        return self._type

    def _validate_role(self, role):
        """
        Validates that the role parameter has a valid value.

        :param role: Name of the column's role
        :type role: str
        """
        valid_roles = ["Input",
                       "Output",
                       "Latent Variable",
                       "Ignore",
                       "input",
                       "output",
                       "latentVariable",
                       "ignore"]
        if role not in valid_roles:
            raise CitrinationClientError("Column role must be one of: {}".format(valid_roles))
