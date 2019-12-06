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
            raise ValueError("Currently, 'lolo' is the only allowed relation type")

        relation_obj['type'] = relation_type

        # check for duplicate
        relation_obj['inputs'].sort()
        existing_relations = self.configuration['relations']
        for ele in existing_relations:
            ele['inputs'].sort() # make sure they are sorted first
            if ele['inputs'] == relation_obj['inputs'] and \
                    ele['output'] == relation_obj['output']:
                raise ValueError("This relation duplicates an existing relation")

        # check limits
        if len(existing_relations) > MAX_USER_RELATIONS:
            raise ValueError("Maximum Relations Reached: Citrination only supports " + str(MAX_USER_RELATIONS) +
                             " user-defined relations. Please review the existing relations")

        # simplify descriptor testing
        descriptor_set = set()
        for desc in self.configuration['descriptors']:
            descriptor_set.add(desc['descriptor_key'])

        # check inputs exist
        for relation_input in relation_obj['inputs']:
            if relation_input not in descriptor_set:
                raise ValueError("Input " + relation_input + " is not defined as a descriptor")
            if relation_obj['inputs'].count(relation_input) > 1:
                raise ValueError("Input " + relation_input + " is listed more than once")
            if relation_input == output:
                raise ValueError("Output " + output + " is also an input")

        if output not in descriptor_set:
            raise ValueError("Output " + output + " is not defined as a descriptor")

        # check duplicate input

        self.configuration['relations'].append(relation_obj)

    def getDagreGraph(self):
        """
        Function to generate a DAGRE graph based on the descriptors and relations added to the builder
        """
        nodes = []
        edges = []

        for desc in self.configuration['descriptors']:
            nodes.append({
                'label': desc['descriptor_key'],
                'attributes': {
                    'style': {
                        'fill': '#ff8200',
                        'stroke': '#453536'
                    }
                }
            })
        for relation in self.configuration['relations']:
            for input_key in relation['inputs']:
                edges.append({
                    "source": input_key,
                    "target": relation['output']
                })
        return {
            "nodes": nodes,
            "edges": edges
        }

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
