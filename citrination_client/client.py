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
    """
    The top level of the client hierarchy. Instantiating this class handles
    authentication information (api_key and site) and provides access to instances of each of the sub-clients, for more specific actions.

    Instantiation requires authentication information, but that can be provided
    via direct parameterization, environment variables, or a .citrination credentials file. See the tutorial on client Initialization for more information.
    """

    def __init__(self, api_key=None, site=None, suppress_warnings=False):
        """
        Constructor.

        :param api_key: Your API key for Citrination
        :type api_key: str
        :param site: The domain name of your Citrination deployment
            (the default is https://citrination.com)
        :type site: str
        :param suppress_warnings: A flag allowing you to suppress warning
            statements guarding against misuse printed to stdout.
        :type suppress_warnings: bool
        """
        api_key, site = get_preferred_credentials(api_key, site)
        self.models = ModelsClient(api_key, site, suppress_warnings=suppress_warnings)
        self.search = SearchClient(api_key, site, suppress_warnings=suppress_warnings)
        self.data = DataClient(api_key, site, suppress_warnings=suppress_warnings)

        clients = [self.models, self.search, self.data]

        for client in clients:
            client_methods = [a for a in dir(client) if not a.startswith('_')]
            for method in client_methods:
                setattr(self, method, _generate_lambda_proxy_method(client, method))


    def __repr__(self):
        return "['models', 'search', 'data']"