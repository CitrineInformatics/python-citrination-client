# ... client initialization left out
data_client = client.data

ingester_list = data_client.list_ingesters()
csv_ingester = ingester_list.find_by_id("citrine/ingest template_csv_converter")
