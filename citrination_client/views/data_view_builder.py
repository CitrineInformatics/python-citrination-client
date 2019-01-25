class DataViewBuilder(object):
    """
    A low dimensional interface for building data views.  Choose datasets, add descriptors and other configuration
    options, then call build() to return the configuration object needed by the data views api
    """

    def __init__(self):
        self.configuration = dict(
            builder='simple',
            dataset_ids=[],
            user_id=0,
            group_by='',
            model_type='default',
            descriptors=[],
            roles=dict()
        )

    def set_user_id(self, user_id):
        """
        Sets the user_id associated with this view.

        :param user_id: Citrination user_id
        """
        self.configuration['user_id'] = user_id

    def set_dataset_ids(self, dataset_ids):
        """
        Sets the dataset ids to use for the view

        :param dataset_ids: Array of strings, one for each dataset id
        """
        self.configuration['dataset_ids'] = dataset_ids

    def set_group_by(self, group_by):
        """
        Sets the group by used on the front-end

        :param group_by: Array of strings for the grouping
        """
        self.configuration['group_by'] = group_by

    def set_model_type(self, model_type):
        """
        Sets the model type for the view

        :param model_type: A string of either linear, or default
        """
        self.configuration['model_type'] = model_type

    def set_role(self, descriptor_key, role):
        """
        Sets the role of a descriptor by key

        :param descriptor_key: The descriptor to set the role for
        :param role: input, output, latentVariable, or ignored
        """
        self.configuration['roles'][descriptor_key] = role

    def add_real_descriptor(self, descriptor_key, upper_bound, lower_bound, role=None):
        """
        Add a real valued descriptor to the configuration

        :param descriptor_key: Identifier for the descriptor
        :param upper_bound: Numeric maximum value
        :param lower_bound: Numeric minimum value
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        descriptor = dict(
            category='Real',
            descriptor_key=descriptor_key,
            upper_bound=upper_bound,
            lower_bound=lower_bound
        )
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor_key, role)

    def add_categorical_descriptor(self, descriptor_key, descriptor_values, role=None):
        """
        Add a categorical valued descriptor to the configuration

        :param descriptor_key: Identifier for the descriptor
        :param descriptor_values: An array of strings
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        descriptor = dict(
            category='Categorical',
            descriptor_key=descriptor_key,
            descriptor_values=descriptor_values
        )
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor_key, role)

    def add_organic_descriptor(self, descriptor_key, role=None):
        """
        Add an organic valued descriptor to the configuration

        :param descriptor_key: Identifier for the descriptor
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        descriptor = dict(
            category='Organic',
            descriptor_key=descriptor_key
        )
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor_key, role)

    def add_alloy_composition_descriptor(self, descriptor_key, balance_element, basis, threshold, role=None):
        """
        Add an alloy composition descriptor to the configuration

        :param descriptor_key: Identifier for the descriptor
        :param balance_element: The element the basis is applied to
        :param basis: Percentage of the balance_element
        :param threshold: Allowable deviation from basis
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        descriptor = dict(
            category='Alloy composition',
            descriptor_key=descriptor_key,
            balance_element=balance_element,
            basis=basis,
            threshold=threshold
        )
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor_key, role)

    def add_inorganic_descriptor(self, descriptor_key, threshold, role=None):
        """
        Add an inorganic valued descriptor to the configuration

        :param descriptor_key: Identifier for the descriptor
        :param threshold: The closeness to an interpretable chemical formula that is accepted as valid
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        descriptor = dict(
            category='Inorganic',
            descriptor_key=descriptor_key,
            threshold=threshold
        )
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor_key, role)

    def add_descriptor(self, descriptor, role=None):
        """
        Add a generic descriptor entry.

        :param descriptor: Descriptor dict, see add_*_descriptor methods in this class for examples
        :param role: Optionally specify a role (input, output, latentVariable, or ignored)
        """
        self.configuration['descriptors'].append(descriptor)
        if role is not None:
            self.set_role(descriptor['descriptor_key'], role)

    def build(self):
        return self.configuration
