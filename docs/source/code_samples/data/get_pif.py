# ... client initialization left out
data_client = client.data
dataset_id = 1

# Gets a single file named exactly my_file.json

data_client.get_pif(dataset_id, "1DF1C8EB706363DS2G3")

# -> {u'category': u'system.chemical', u'uid': u'1DF1C8EB706363....