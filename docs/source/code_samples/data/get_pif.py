# ... client initialization left out
data_client = client.data
dataset_id = 1
pif_uid = "abc123"

# Retrieves the latest version of the PIF with uid is "abc123" from the latest
# version of dataset 1
data_client.get_pif(dataset_id, pif_uid)

# Retrieves the latest version of the PIF with uid is "abc123" from version 3
# of dataset 1
data_client.get_pif(dataset_id, pif_uid, dataset_version = 3)

# Retrieves the version 2 of the PIF with uid is "abc123" from the latest version
# of dataset 1
data_client.get_pif(dataset_id, pif_uid, pif_version = 2)

# Retrieves the version 2 of the PIF with uid is "abc123" from version 3 of
# dataset 1
data_client.get_pif(dataset_id, pif_uid, dataset_version = 3, pif_version = 2)
