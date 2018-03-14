# ... client initialization left out
data_client = client.data
dataset_id = 1

# Gets a single file named exactly my_file.json

data_client.get_dataset_file(dataset_id, "my_file.json")

# {'file': {'url': "my.file.url.com", 'filename': 'test_directory_upload/weird_extensions.woodle'}}

# Gets all the files in a dataset, organized by version

data_client.get_dataset_files(dataset_id)

# {'versions': [
#   {'files': [
#     {
#       'url': 'my.file.url.com',
#       'filename': 'my_file.json'
#     }]
#   }...]
# }

# Gets all the files matched 