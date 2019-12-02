MAX_USER_RELATIONS = 30

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
            relations=[],
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

    def add_relation(self, inputs, output, relation_type='lolo'):
        """
        Add a manual relation.  If no relations are manually added, Citrination will automatically generate
        relations when the view is created.

        :param inputs: Array of strings or a single string of descriptor key(s) for the relation inputs
        :param output: Single string descriptor key for the relation output
        :param relation_type: Kind of relation, currently only 'lolo' is supported
        """
        relation_obj = {}

        if isinstance(inputs, str):
            relation_obj['inputs'] = [inputs]
        elif isinstance(inputs, list):
            if len(inputs) == 0:
                raise ValueError("Inputs list must not be empty")
            relation_obj['inputs'] = inputs
        else:
            raise ValueError("Unexpected type for inputs, expecting either a string or list of strings")

        if isinstance(output, str):
            relation_obj['output'] = output
        else:
            raise ValueError("Unexpected type for output, expecting a string")

        if relation_type != 'lolo':
            raise ValueError("Currently, \'lolo\' is the only allowed relation type")

        relation_obj['type'] = relation_type

        # check for duplicate
        existing_relations = self.configuration['relations']
        for pos, ele in enumerate(existing_relations):
            if existing_relations[pos]['inputs'] == relation_obj['inputs'] and \
                    existing_relations[pos]['output'] == relation_obj['output']:
                raise ValueError("This relation duplicates an existing relation")

        # check limits
        if len(existing_relations) > MAX_USER_RELATIONS:
            raise ValueError("Maximum Relations Reached: Citrination only supports " + str(MAX_USER_RELATIONS) +
                             " user-defined relations. Please review the existing relations")

        # check inputs exist
        for input_index, input in enumerate(relation_obj['inputs']):
            found = False
            for desc_index, desc in enumerate(self.configuration['descriptors']):
                if desc['descriptor_key'] == input:
                    found = True
                    break
            if not found:
                raise ValueError("Input " + input + " is not defined as a descriptor")

        found = False
        for desc_index, desc in enumerate(self.configuration['descriptors']):
            if desc['descriptor_key'] == output:
                found = True
                break
        if not found:
            raise ValueError("Output " + output + " is not defined as a descriptor")


        self.configuration['relations'].append(relation_obj)

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
