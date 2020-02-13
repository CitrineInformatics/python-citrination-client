advanced_config = advanced_builder.build()

# Create a data view
data_view_id = client.data_views.create(
    advanced_config, 'My dataview name', 'The data view description'
)

# Or update an existing data view
client.update(data_view_id, advanced_config)
