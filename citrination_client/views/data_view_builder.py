from citrination_client.views.base_data_view_builder import BaseDataViewBuilder

class DataViewBuilder(BaseDataViewBuilder):
    """
    A low dimensional interface for building data views.  Choose datasets, add
    descriptors and other configuration options, then call build() to return the
    configuration object needed by the data views api

    Inherits from the BaseDataViewBuilder
    """

    def __init__(self):
        super(DataViewBuilder, self).__init__(
            { 'builder': 'simple', 'roles': dict() }
        )

    def add_descriptor(self, descriptor, role='ignore', group_by_key=False):
        """
        Add a descriptor column.

        :param descriptor: A Descriptor instance (e.g., RealDescriptor, InorganicDescriptor, etc.)
        :param role: Specify a role (input, output, latentVariable, or ignore)
        :param group_by_key: Whether or not to group by this key during cross validation
        """

        descriptor.validate()

        if descriptor.key in self.configuration["roles"]:
            raise ValueError("Cannot add a descriptor with the same name twice")

        self.configuration['descriptors'].append(descriptor.as_dict())
        self.configuration["roles"][descriptor.key] = role

        if group_by_key:
            self.configuration["group_by"].append(descriptor.key)

    def set_role(self, key, role):
        """
        Sets the role of a descriptor

        :param key: A descriptor key
        :type key: str
        :param role: (input, output, latentVariable, or ignore)
        :type role: str
        """
        self.configuration['roles'][key] = role

    def _add_role_if_required(self, key, role):
        """
        Overridden from base class.  The normal builder will set roles

        :param key: descriptor key
        :param role: ignore, input, output, or latentVariable
        """
        self.set_role(key, role)

