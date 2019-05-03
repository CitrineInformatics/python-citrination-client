from citrination_client import RealDescriptor, AlloyCompositionDescriptor
from citrination_client.views.data_view_builder import DataViewBuilder

dv_builder = DataViewBuilder()
dv_builder.dataset_ids(29)
desc = RealDescriptor(u'Property Bulk modulus',
                      '0', '10000')
dv_builder.add_descriptor(desc, 'output')
desc = AlloyCompositionDescriptor('formula', 'ALUMINUM')
dv_builder.add_descriptor(desc, 'input')
dv_config = dv_builder.build()

# Create the data view
data_view_id = data_views_client.create(dv_config, 'My dataview name', 'The data view description')