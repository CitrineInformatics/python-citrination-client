# ... client initialization left out
data_client = client.data

# Creates a new dataset (permissions default to private)
dataset = data_client.create_dataset("My New Dataset")
dataset_id = dataset.id

# Make the dataset public
data_client.update_dataset(dataset_id, public=True)

# Make the dataset private again
data_client.update_dataset(dataset_id, public=False)
