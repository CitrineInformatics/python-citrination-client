# ... client initialization left out
data_client = client.data

file_path = "experiments/data.xrdml"
dataset_id = 1

ingester_list = data_client.list_ingesters()
xrdml_ingester = ingester_list.find_by_id("citrine/ingest xrdml_xrd_converter")

# Printing the ingester's arguments, we can see it requires an argument with the
# name `sample_id`, and another with the name `chemical_formula`, both of which
# should be strings.
print(ingester.arguments)
# [{ 'name': 'sample_id',
#    'desc': 'An ID to uniquely identify the material referenced in the file.',
#    'type': 'String',
#    'required': True },
#  { 'name': 'chemical_formula',
#    'desc': 'The chemical formula of the material referenced in the file.',
#    'type': 'String',
#    'required': True }]

ingester_arguments = [
    { "name": "sample_id", "value": "1212" },
    { "name": "chemical_formula", "value": "NaCl" },
]

# To ingest the file using the file_path as the destination path
data_client.upload_with_ingester(
    dataset_id, file_path, xrdml_ingester, ingester_arguments
)
# To ingest the file using a different destination path
data_client.upload_with_ingester(
    dataset_id, file_path, xrdml_ingester, ingester_arguments, 'data.xrdml'
)
