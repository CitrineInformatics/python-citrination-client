# ... client initialization left out
data_client = client.data

dataset = client.data.create_dataset()
file = 'test_data/template_example.csv'
client.data.upload_with_template_csv_ingester(dataset.id, file)

# After uploading, the status will initially be `Processing`
print(client.data.get_ingest_status(dataset.id))
# Processing

# After data has finished processing, the status will be `Finished`
print(client.data.get_ingest_status(dataset.id))
# Finished
