class DataViewBuilder(object):
    """
    A low dimensional interface for building data views.  Choose datasets, add descriptors and other configuration
    options, then call build() to return the configuration object needed by the data views api
    """

    def __init__(self):
        self.configuration = dict(
            builder='simple',
            dataset_ids=[],
            group_by=[],
            model_type='default',
            descriptors=[],
            roles=dict()
        )

    def dataset_ids(self, dataset_ids):
        """
        Sets the dataset ids to use for the view

        :param dataset_ids: Array of strings, one for each dataset id
        """
        self.configuration['dataset_ids'] = dataset_ids

    def model_type(self, model_type):
        """
        Sets the model type for the view

        :param model_type: A string of either linear (for a linear model), or default (for Citrine's default nonlinear model)
        """
        self.configuration['model_type'] = model_type

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

    def add_raw_descriptor(self, descriptor):
        """
        Add a raw descriptor dictionary object.

        :param descriptor: A descriptor as a dictionary
        """
        self.configuration['descriptors'].append(descriptor)

    def set_role(self, key, role):
        """
        Sets the role of a descriptor

        :param key: A descriptor key
        :type key: str
        :param role: (input, output, latentVariable, or ignore)
        :type role: str
        """
        self.configuration['roles'][key] = role

    def build(self):
        """
        Returns a configuration object suitable for creating a data view.

        :return: See __init__ method for returned dict shape
        :rtype: :dict
        """
        return self.configuration
