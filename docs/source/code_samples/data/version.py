# ... client initialization left out
data_client = client.data

# Creates a new dataset (permissions default to private)
dataset = data_client.create_dataset("My New Dataset")
dataset_id = dataset.id

# Uploads a file to it
data_client.upload(dataset_id, "my_file.json")

print(data_client.matched_file_count(dataset_id))
# -> 1

# Create a new dataset version
data_client.create_dataset_version(dataset_id)

# No files in the new version
print(data_client.matched_file_count(dataset_id))
# -> 0