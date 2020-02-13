from citrination_client.views.client import DataViewsClient
from os import environ

# Note: for the purposes of this example, environ["CITRINATION_SITE"] is
#       https://citrination.com
client = DataViewsClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

dataset_ids = ['1160']
# Get the ml config defaults for all descriptor keys in the datasets
data_view_config = client.create_ml_configuration_from_datasets(dataset_ids)

print(data_view_config)
# {
#   "dataset_ids": [
#     1160
#   ],
#   "group_by": [],
#   "model_type": "default",
#   "descriptors": [
#     {
#       "category": "Real",
#       "descriptor_key": "Temperature (Property Thermoluminescence)",
#       "units": "",
#       "lower_bound": 0,
#       "upper_bound": 1746
#     },
#     {
#       "category": "Categorical",
#       "descriptor_key": "Property Crystallinity",
#       "descriptor_values": [
#         "Single crystalline",
#         "Polycrystalline",
#         "Amorphous"
#       ],
#       "finite_set": True
#     },
#     ...
#           (truncated for documentation)
#     ...
#   ],
#   "builder": "simple",
#   "roles": {
#     "Temperature (Property Thermoluminescence)": "input",
#     "Property Temperature derivative of band gap": "output",
#     "Property Crystallinity": "output",
#     "Electric field polarization (Property Band gap)": "input",
#     ...
#          (truncated for documentation)
#     ...
#   }
# }
