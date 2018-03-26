# ... client initialization left out
data_client = client.data

# Creates a new dataset (permissions default to private)
dataset = data_client.create_dataset("My New Dataset")
dataset_id = dataset["id"]

# Uploads a file to it
data_client.upload(dataset_id, "my_file.json")

# Make the dataset public
data_client.update_dataset(dataset_id, public=True)

# Make the dataset private again
data_client.update_dataset(dataset_id, public=False)

print(data_client.matched_file_count(dataset_id))
# -> 1

data_client.create_dataset_version(dataset_id)

# No files in the new version
print(data_client.matched_file_count(dataset_id))
# -> 0