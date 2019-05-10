from citrination_client.views.search_template.client import SearchTemplateClient
from os import environ

client = SearchTemplateClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

# Get an array of descriptor keys for dataset id 29
res = client.get_available_columns('29')
print(res)
# ['formula', 'Property Bulk modulus']