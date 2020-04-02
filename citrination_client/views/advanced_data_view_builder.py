from citrination_client.views.base_data_view_builder import BaseDataViewBuilder
from citrination_client.views.descriptors import CategoricalDescriptor
from citrination_client.views.descriptors import RealDescriptor
import re

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

    def add_formulation_descriptor(self, descriptor, dataview_client):
        """
        Add a formulation descriptor and automatically add ignored ingredient shares, component type and
        name categorical descriptors.

        :param descriptor: The formulation descriptor to add
        :param dataview_client: The dataview client, this is needed to obtain the ingredient share names
        """

        self.add_descriptor(descriptor)
        self.add_descriptor(CategoricalDescriptor("name",["*"]))
        self.add_descriptor(CategoricalDescriptor("component type", ["*"]))

        # Use template client to find the % share descriptors
        if self.configuration['dataset_ids']:
            client = dataview_client.search_template_client
            cols = client.get_available_columns(self.configuration['dataset_ids'])
            for col in cols:
                if re.match("% .* \(\w, \w\)",col):
                    self.add_descriptor(RealDescriptor(col))



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
