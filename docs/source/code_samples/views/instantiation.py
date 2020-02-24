from citrination_client import CitrinationClient
from os import environ

client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
data_views_client = client.data_views

# Alternatively, import and instantiate the data views client directly
from citrination_client.views.client import DataViewsClient
data_views_client = DataViewsClient(
    environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"]
)
