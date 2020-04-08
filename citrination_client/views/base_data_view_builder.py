from citrination_client.views.descriptors import CategoricalDescriptor
from citrination_client.views.descriptors import RealDescriptor
import re


class BaseDataViewBuilder(object):
    """
    A base class not intended to be instantiated directly.
    """

    def __init__(self, additional_config):
        self.configuration = dict(
            dataset_ids=[],
            group_by=[],
            model_type='default',
            descriptors=[]
        )
        self.configuration.update(additional_config)

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

    def add_raw_descriptor(self, descriptor):
        """
        Add a raw descriptor dictionary object.

        :param descriptor: A descriptor as a dictionary
        """
        self.configuration['descriptors'].append(descriptor)

    def get_dagre_graph(self):
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

    def _add_role_if_required(self, key, role):
        """
        Overridden by derived class if roles are being used

        :param key: descriptor key
        :param role: ignore, input, output, or latentVariable
        """
        # intentionally does nothing

    def add_formulation_descriptor(self, descriptor, dataview_client):
        """
        Add a formulation descriptor and automatically add ignored ingredient shares, component type and
        name categorical descriptors.

        :param descriptor: The formulation descriptor to add
        :param dataview_client: The dataview client, this is needed to obtain the ingredient share names
        """

        self.add_descriptor(descriptor)
        self._add_role_if_required(descriptor.key, "input")
        self.add_descriptor(CategoricalDescriptor("name", ["*"]))
        self._add_role_if_required("name", "ignore")
        self.add_descriptor(CategoricalDescriptor("component type", ["*"]))
        self._add_role_if_required("component type", "ignore")

        # Use template client to find the % share descriptors
        if self.configuration['dataset_ids']:
            client = dataview_client.search_template_client
            cols = client.get_available_columns(self.configuration['dataset_ids'])
            for col in cols:
                if re.match("% .* \(\w*, \w*\)", col):
                    self.add_descriptor(RealDescriptor(col, 0, 1))
                    self._add_role_if_required(col, "ignore")

    def build(self):
        """
        Returns a configuration object suitable for creating a data view.

        :return: See __init__ method for returned dict shape
        :rtype: :dict
        """
        return self.configuration
