from citrination_client.models import ModelsClient
from citrination_client.search import SearchClient
from citrination_client.data import DataClient

class CitrinationClient(object):

  def __init__(self, api_key, host="https://citrination.com"):
    self.models = ModelsClient(api_key, host)
    self.search = SearchClient(api_key, host)
    self.data = DataClient(api_key, host)

  def __repr__(self):
    return "['models', 'search', 'data']"