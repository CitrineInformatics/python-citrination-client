from citrination_client.models import ModelsClient
from citrination_client.search import SearchClient
from citrination_client.data import DataClient
from citrination_client.util.credentials import get_preferred_credentials

class CitrinationClient(object):

    def __init__(self, api_key=None, site=None):
        api_key, site = get_preferred_credentials(api_key, site)
        self.models = ModelsClient(api_key, site)
        self.search = SearchClient(api_key, site)
        self.data = DataClient(api_key, site)

    def __repr__(self):
        return "['models', 'search', 'data']"