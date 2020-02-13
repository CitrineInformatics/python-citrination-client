from citrination_client.views.advanced_data_view_builder import AdvancedDataViewBuilder
from citrination_client.views.client import DataViewsClient
from os import environ

client = DataViewsClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

dataset_ids = ['1160']
# Get the ml config defaults for all descriptor keys in the datasets
data_view_config = client.create_ml_configuration_from_datasets(dataset_ids)

descriptor_keys = [
    'formula',
    'Property Band gap',
    'Property Color',
    'Temperature (Property Band gap)',
    'Temperature (Property Color)'
]
descriptors = list(
    filter(
        lambda d: d['descriptor_key'] in descriptor_keys,
        data_view_config['descriptors']
    )
)
