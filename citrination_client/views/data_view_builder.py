class DataViewBuilder(object):
    """
    A low dimensional interface for building data views.  Choose datasets, add descriptors and other configuration
    options, then call build() to return the configuration object needed by the data views api
    """

    def __init__(self):
        self.configuration = dict(
            builder='simple',
            dataset_ids=[],
            userId=0,
            groupBy='',
            modelType='default',
            descriptors=[],
            roles=dict()
        )

    def set_userId(self, userId):
        """
        Sets the userId associated with this view.

        :param userId: Citrination userid
        """
        self.configuration['userId'] = userId

    def set_datasetIds(self, datasetIds):
        """
        Sets the dataset ids to use for the view

        :param datasetIds: Array of strings, one for each dataset id
        """
        self.configuration['dataset_ids'] = datasetIds

    def set_groupBy(self, groupBy):
        """
        Sets the group by used on the front-end

        :param groupBy: Array of strings for the grouping
        """
        self.configuration['groupBy'] = groupBy

    def set_modelType(self, modelType):
        """
        Sets the model type for the view

        :param modelType: A string of either linear, or default
        """
        self.configuration['modelType'] = modelType

    def set_role(self, descriptorKey, role):
        """
        Sets the role of a descriptor by key

        :param descriptorKey: The descriptor to set the role for
        :param role: input, output, latentVariable, or ignored
        """
        self.configuration['roles'][descriptorKey] = role

    def add_real_descriptor(self, descriptorKey, upper_bound, lower_bound, units):
        """
        Add a real valued descriptor to the configuration

        :param descriptorKey: Identifier for the descriptor
        :param upper_bound: Numeric maximum value
        :param lower_bound: Numeric minimum value
        :param units: Units to use for values for this column
        """
        descriptor = dict(
            category='Real',
            descriptorKey=descriptorKey,
            upper_bound=upper_bound,
            lower_bound=lower_bound,
            units=units
        )
        self.configuration['descriptors'].append(descriptor)

    def add_categorical_descriptor(self, descriptorKey, descriptorValues):
        """
        Add a categorical valued descriptor to the configuration

        :param descriptorKey: Identifier for the descriptor
        :param descriptorValues: An array of strings
        """
        descriptor = dict(
            category='Categorical',
            descriptorKey=descriptorKey,
            descriptorValues=descriptorValues
        )
        self.configuration['descriptors'].append(descriptor)

    def add_organic_descriptor(self, descriptorKey):
        """
        Add an organic valued descriptor to the configuration

        :param descriptorKey: Identifier for the descriptor
        """
        descriptor = dict(
            category='Organic',
            descriptorKey=descriptorKey
        )
        self.configuration['descriptors'].append(descriptor)

    def add_alloy_composition_descriptor(self, descriptorKey, balanceElement, basis, threshold):
        """
        Add an alloy composition descriptor to the configuration

        :param descriptorKey: Identifier for the descriptor
        :param balanceElement: The element the basis is applied to
        :param basis: Percentage of the balanceElement
        :param threshold: Allowable deviation from basis
        """
        descriptor = dict(
            category='Alloy composition',
            descriptorKey=descriptorKey,
            balanceElement=balanceElement,
            basis=basis,
            threshold=threshold
        )
        self.configuration['descriptors'].append(descriptor)

    def add_inorganic_descriptor(self, descriptorKey, threshold):
        """
        Add an inorganic valued descriptor to the configuration

        :param descriptorKey: Identifier for the descriptor
        :param threshold: The closeness to an interpretable chemical formula that is accepted as valid
        """
        descriptor = dict(
            category='Inorganic',
            descriptorKey=descriptorKey,
            threshold=threshold
        )
        self.configuration['descriptors'].append(descriptor)

    def build(self):
        return self.configuration
