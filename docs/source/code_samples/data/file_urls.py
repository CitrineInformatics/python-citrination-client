# ... client initialization left out
data_client = client.data
dataset_id = 1

# Gets a single file named exactly my_file.json

data_client.get_dataset_file(dataset_id, "my_file.json")

# Returns a DatasetFile object

# Gets all the files in a dataset, organized by version,
# represented as a list of DatasetFile objects

data_client.get_dataset_files(dataset_id)