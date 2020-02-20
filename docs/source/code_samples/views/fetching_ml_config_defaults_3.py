print(data_view_config)
# {   'dataset_ids': ['1160'],
#     'group_by': [],
#     'model_type': 'default',
#     'descriptors': [
#         {
#             'category': 'Real',
#             'descriptor_key': 'Temperature (Property Band gap)',
#             'units': '',
#             'lower_bound': 0.0,
#             'upper_bound': 1946.0
#         }, {
#             'category': 'Categorical',
#             'descriptor_key': 'Property Color',
#             'descriptor_values': [
#                 'Yellow', 'Pale Yellow', 'Violet', 'Gray', 'Amber', 'Orange-Red',
#                 'Dark Brown', 'Red', 'Blue', 'White', 'Red-Yellow', 'Brown',
#                 'Black', 'Ocher', 'Bluish', 'Bronze', 'Light Gray', 'Dark Green',
#                 'Yellow-White', 'Copper-Red', 'Brown-Black', 'Yellow-Orange',
#                 'Orange', 'Dark Gray', 'Dark Red'
#             ],
#             'finite_set': True
#         }, {
#             'category': 'Real',
#             'descriptor_key': 'Temperature (Property Color)',
#             'units': '',
#             'lower_bound': 0.0,
#             'upper_bound': 1746.0
#         }, {
#             'category': 'Real',
#             'descriptor_key': 'Property Band gap',
#             'units': '',
#             'lower_bound': 0.0,
#             'upper_bound': 29.0
#         }, {
#             'category': 'Inorganic',
#             'descriptor_key': 'formula',
#             'threshold': 1.0
#         }
#     ],
#     'builder': 'simple',
#     'roles': {
#         'formula': 'input',
#         'Property Band gap': 'output',
#         'Property Color': 'output',
#         'Temperature (Property Band gap)': 'input',
#         'Temperature (Property Color)': 'input'
#     }
# }

# Create a data view
data_view_id = client.create(
    data_view_config, 'My dataview name', 'The data view description'
)

# Or update an existing data view
client.update(data_view_id, data_view_config)
