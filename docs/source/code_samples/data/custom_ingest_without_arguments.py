# ... client initialization left out
data_client = client.data

file_path = "data/formulation.csv"
dataset_id = 1

ingester_list = data_client.list_ingesters()
formulation_ingester = ingester_list.find_by_id("citrine/ingest formulation_csv_converter")

# Printing the formulation_ingester's arguments, we can see that it takes one
# argument that is optional - so we can elect to omit it
print(formulation_ingester.arguments)
# [{ 'name': 'check_ingredient_names',
#    'desc': 'Whether to check that the names of the ingredients in the formulations are present in this upload',
#    'type': 'Boolean',
#    'required': False }]

# To ingest the file using the file_path as the destination path
data_client.upload_with_ingester(
    dataset_id, file_path, formulation_ingester
)
# To ingest the file using a different destination path
data_client.upload_with_ingester(
    dataset_id, file_path, formulation_ingester, dest_path='formulation.csv'
)
