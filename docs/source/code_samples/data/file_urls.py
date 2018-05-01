# ... client initialization left out
data_client = client.data
dataset_id = 1

# Gets a single file named exactly my_file.json

dataset_file = data_client.get_dataset_file(dataset_id, "my_file.json")

dataset_file.url  # url that can be used to download the file
dataset_file.path # the filepath as it appears in Citrination

# Gets all the files in a dataset, organized by version,
# represented as a list of DatasetFile objects

dataset_files = data_client.get_dataset_files(dataset_id)
