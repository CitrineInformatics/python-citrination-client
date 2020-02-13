from citrination_client import CategoricalDescriptor, InorganicDescriptor, RealDescriptor
from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.client import DataViewsClient
from os import environ

# Note: for the purposes of this example, environ["CITRINATION_SITE"] is
#       https://citrination.com
client = DataViewsClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

dv_builder = DataViewBuilder()
dv_builder.dataset_ids([1160])

colors = [
    'Yellow', 'Pale Yellow', 'Violet', 'Gray', 'Amber', 'Orange-Red', 'Dark Brown',
    'Red', 'Blue', 'White', 'Red-Yellow', 'Brown', 'Black', 'Ocher', 'Bluish',
    'Bronze', 'Light Gray', 'Dark Green', 'Yellow-White', 'Copper-Red',
    'Brown-Black', 'Yellow-Orange', 'Orange', 'Dark Gray', 'Dark Red'
]

dv_builder.add_descriptor(
    InorganicDescriptor('formula'), 'input'
)
dv_builder.add_descriptor(
    RealDescriptor('Temperature (Property Band gap)', '0.0', '1946.0'), 'input'
)
dv_builder.add_descriptor(
    RealDescriptor('Temperature (Property Color)', '0.0', '1946.0'), 'input'
)
dv_builder.add_descriptor(
    RealDescriptor(u'Property Band gap', '0.0', '29.0'), 'latentVariable'
)
dv_builder.add_descriptor(
    CategoricalDescriptor(u'Property Color', colors), 'output'
)

# Converts the DataViewBuilder instance to a dictionary "config" object
data_view_config = dv_builder.build()

# Create a data view
data_view_id = client.create(
    data_view_config, 'My dataview name', 'The data view description'
)

# Or update an existing data view
client.update(data_view_id, data_view_config)
