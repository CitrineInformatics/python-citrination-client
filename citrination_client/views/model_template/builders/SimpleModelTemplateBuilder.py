
class SimpleModelTemplateBuilder(object):
    """
    A low dimensional interface for building model templates, based on a basic "ml config" object that specifies
    descriptor types and basic input/output roles for each column.
    """

    def __init__(self):
        self.descriptors = dict()

    def add_real_descriptor(self, column_name, role, upper_bound, lower_bound, units=None):
        """
        Add a real valued descriptor to the configuration

        :param column_name: Name of the column this descriptor applies to
        :param role: Input, Output, or LatentVariable
        :param upper_bound: Numeric maximum value
        :param lower_bound: Numeric minimum value
        :param units: Units to use for values for this column
        """
        descriptor = dict(
            role=role,
            descriptor=dict(
                category='Real',
                upperBound=upper_bound,
                lowerBound=lower_bound
            )
        )
        if units is not None:
            descriptor['descriptor'].update(units=units)
        self.descriptors.update({column_name: descriptor})

    def add_categorical_descriptor(self, column_name, role, descriptorValues, finiteSet):
        """
        Add a categorical valued descriptor to the configuration

        :param column_name: Name of the column this descriptor applies to
        :param role: Input, Output, or LatentVariable
        :param descriptorValues: An array of categories
        :param finiteSet: True if the set given is exhaustive, False if not
        """
        descriptor = dict(
            role=role,
            descriptor=dict(
                category='Categorical',
                descriptorValues=descriptorValues,
                finiteSet=finiteSet
            )
        )
        self.descriptors.update({column_name: descriptor})

    def add_organic_descriptor(self, column_name, role, threshold=None):
        """
        Add an organic valued descriptor to the configuration

        :param column_name: Name of the column this descriptor applies to
        :param role: Input, Output, or LatentVariable
        :param threshold: Numeric threshold
        """
        descriptor = dict(
            role=role,
            descriptor=dict(
                category='Organic',
            )
        )
        if threshold is not None:
            descriptor['descriptor'].update(threshold=threshold)
        self.descriptors.update({column_name: descriptor})

    def build(self):
        return self.descriptors

