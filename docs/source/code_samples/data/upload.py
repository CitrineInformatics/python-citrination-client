from citrination_client import CitrinationClient
from os import environ

client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
data_client = client.data

file_path = "characterizations/CdTe1.json"
dataset_id = 1
data_client.upload(1, file_path)