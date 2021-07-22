from citrination_client.views.client import DataViewsClient
from os import environ

# Note: for the purposes of this example, environ["CITRINATION_SITE"] is
#       https://citrination.com
client = DataViewsClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

# Get an array of descriptor keys for dataset id 1160
dataset_ids = ['1160']
descriptor_keys = client.search_template_client.get_available_columns(dataset_ids)
print(descriptor_keys)

# ['formula',
#  'Property Lasing',
#  'Temperature (Property Lasing)',
#  'Property Electroluminescence',
#  'Temperature (Property Electroluminescence)',
#  'Property Temperature derivative of band gap',
#  'Temperature (Property Temperature derivative of band gap)',
#  'Transition (Property Temperature derivative of band gap)',
#  'Electric field polarization (Property Temperature derivative of band gap)',
#  'Property Phase',
#  'Property Photoluminescence',
#  'Temperature (Property Photoluminescence)',
#  'Property Thermoluminescence',
#  'Temperature (Property Thermoluminescence)',
#  'Property Morphology',
#  'Property Mechanical luminescence',
#  'Temperature (Property Mechanical luminescence)',
#  'Property Cathodoluminescence',
#  'Temperature (Property Cathodoluminescence)',
#  'Property Band gap',
#  'Temperature (Property Band gap)',
#  'Transition (Property Band gap)',
#  'Electric field polarization (Property Band gap)',
#  'Property Crystallinity',
#  'Property Color',
#  'Temperature (Property Color)']
