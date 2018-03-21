from citrination_client.models import ModelsClient
from citrination_client.search import SearchClient
from citrination_client.data import DataClient
from citrination_client.util.credentials import get_preferred_credentials

"""
Generates a lambda method in a closure such that the
client and method_name are constant (avoides reassignment
in the assignment loop in the client class)
"""
def _generate_lambda_proxy_method(client, method_name):
    subclient_m = getattr(client, method_name)
    return lambda *args, **kw: subclient_m(*args, **kw)

class CitrinationClient(object):

    def __init__(self, api_key=None, site=None):
        api_key, site = get_preferred_credentials(api_key, site)
        self.models = ModelsClient(api_key, site)
        self.search = SearchClient(api_key, site)
        self.data = DataClient(api_key, site)

        clients = [self.models, self.search, self.data]

        for client in clients:
            client_methods = [a for a in dir(client) if not a.startswith('_')]
            for method in client_methods:
                setattr(self, method, _generate_lambda_proxy_method(client, method))


    def __repr__(self):
        return "['models', 'search', 'data']"