# ... client initialization left out
data_client = client.data

file_path = "experiments/data.csv"
dataset_id = 1

# To ingest the file using the file_path as the destination path
data_client.upload_with_template_csv_ingester(
    dataset_id, file_path
)
# To ingest the file using a different destination path
data_client.upload_with_template_csv_ingester(
    dataset_id, file_path, dest_path='data.csv'
)
