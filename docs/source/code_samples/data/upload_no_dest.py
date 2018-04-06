# ... client initialization left out
data_client = client.data

file_path = "characterizations/CdTe1.json"
dataset_id = 1
data_client.upload(dataset_id, file_path)