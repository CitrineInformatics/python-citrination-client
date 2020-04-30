advanced_builder = AdvancedDataViewBuilder()
advanced_builder.dataset_ids(dataset_ids)

for descriptor in descriptors:
    advanced_builder.add_raw_descriptor(descriptor)

advanced_builder.add_relation(['formula'], 'Property Band gap')
advanced_builder.add_relation(['formula', 'Temperature (Property Color)'], 'Property Color')
advanced_builder.add_relation(['formula', 'Temperature (Property Band gap)'], 'Property Band gap')
advanced_builder.add_relation(['formula', 'Property Band gap'], 'Property Color')
