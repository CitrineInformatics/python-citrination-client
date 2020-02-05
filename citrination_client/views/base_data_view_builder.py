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

    def build(self):
        """
        Returns a configuration object suitable for creating a data view.

        :return: See __init__ method for returned dict shape
        :rtype: :dict
        """
        return self.configuration
