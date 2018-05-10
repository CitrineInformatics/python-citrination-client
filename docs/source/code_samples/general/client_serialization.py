client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])

print(client)
# ['models', 'search', 'data']

models_client = client.models
type(models_client)
# <class 'citrination_client.models.client.ModelsClient'>