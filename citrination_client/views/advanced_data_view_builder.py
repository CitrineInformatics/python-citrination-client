from citrination_client.views.base_data_view_builder import BaseDataViewBuilder

MAX_USER_RELATIONS = 30

class AdvancedDataViewBuilder(BaseDataViewBuilder):
    """
    A more expressive interface for building data views with machine learning. Choose
    datasets, add descriptors, and specify relations, then call build() to
    return the configuration object needed by the data views API.

    Inherits from the BaseDataViewBuilder
    """

    def __init__(self):
        super(AdvancedDataViewBuilder, self).__init__(
            { 'builder': 'relation', 'relations': [] }
        )

    def add_descriptor(self, descriptor, group_by_key=False):
        """
        Add a descriptor column.

        :param descriptor: A Descriptor instance (e.g., RealDescriptor, InorganicDescriptor, etc.)
        :param group_by_key: Whether or not to group by this key during cross validation
        """
        descriptor.validate()

        self.configuration['descriptors'].append(descriptor.as_dict())

        if group_by_key:
            self.configuration["group_by"].append(descriptor.key)

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
