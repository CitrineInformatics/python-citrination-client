# ... client initialization left out
from dagre_py.core import plot
views_client = client.data_views

# Example using https://citrination.com/data_views/12329/data_summary
# Returns a dict containing `nodes` and `edges`
relation_graph = client.data_views.get_relation_graph(12329)

print(relation_graph)
# {'edges': [{'source': 'formula', 'target': 'ML Model: 1'},
#            {'source': 'ML Model: 1', 'target': 'Property Bulk modulus'}],
#  'nodes': [{'attributes': {'style': {'fill': '#ff8200', 'stroke': '#453536'}},
#             'description': 'Featurized to: \n'
#                            '-- mean of Packing density\n'
#                            '-- mean of Liquid range\n'
#                            '...', (truncated for documentation purposes)
#             'label': 'formula'},
#            {'attributes': {'style': {'fill': '#ff8200', 'stroke': '#453536'}},
#             'description': 'Error Metrics\n'
#                            '- Root mean squared error  (GPa) (0.0 for a '
#                            'perfect model) = 50.427349\n'
#                            '- Uncertainty calibration: root mean square of '
#                            'standardized errors (1.0 is perfectly calibrated) '
#                            '= 2.069455\n'
#                            '...', (truncated for documentation purposes)
#             'label': 'Property Bulk modulus'},
#            {'attributes': {'style': {'fill': '#78be20', 'stroke': '#453536'}},
#             'description': 'Model Type: Lolo\nSample Count: 30\n',
#             'label': 'ML Model: 1'}]}

# Uses ``dagre_py`` to create a visualization of the relation graph in jupyter.
# See screenshot below.
plot(relation_graph)
