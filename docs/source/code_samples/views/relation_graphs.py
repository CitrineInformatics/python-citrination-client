# ... client initialization left out
from dagre_py.core import plot
views_client = client.data_views

# Example using https://citrination.com/data_views/12329/data_summary
# Returns a dict containing `nodes` and `edges`
relation_graph = client.data_views.get_relation_graph(12329)

print(relation_graph)
# {'nodes': [{'label': 'formula',
#    'description': "\n\nFeaturized to: \n-- mean of Packing density\n-- mean of Liquid range\n...",
#    'attributes': {'style': {'fill': '#ff8200', 'stroke': '#453536'}}},
#   {'label': 'lolo:1',
#    'description': '',
#    'attributes': {'style': {'fill': '#78be20', 'stroke': '#453536'}}},
#   {'label': 'Property Bulk modulus',
#    'description': '',
#    'attributes': {'style': {'fill': '#ff8200', 'stroke': '#453536'}}}],
#  'edges': [{'source': 'formula', 'target': 'lolo:1'},
#   {'source': 'lolo:1', 'target': 'Property Bulk modulus'}]}

# Uses ``dagre_py`` to create a visualization of the relation graph in jupyter.
# See screenshot below.
plot(relation_graph)
