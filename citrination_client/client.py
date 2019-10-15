from citrination_client.views.client import DataViewsClient

from citrination_client.models import ModelsClient
from citrination_client.search import SearchClient
from citrination_client.data import DataClient
from citrination_client.util.credentials import get_preferred_credentials

class CitrinationClient(object):
    """
    The top level of the client hierarchy. Instantiating this class handles
    authentication information (api_key and site) and provides access to instances
    of each of the sub-clients, for more specific actions.

    Instantiation requires authentication information, but that can be provided
    via direct parameterization, environment variables, or a .citrination credentials
    file. See the tutorial on client Initialization for more information.
    """

    def __init__(self, api_key=None, site=None, suppress_warnings=False, proxies=None):
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
        :param proxies: proxies to use when making HTTP requests. E.g.,
            proxies = { 'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080' }
        :type proxies: dict(string, string)
        """
        api_key, site = get_preferred_credentials(api_key, site)
        self.models = ModelsClient(api_key, site, suppress_warnings=suppress_warnings, proxies=proxies)
        self.search = SearchClient(api_key, site, suppress_warnings=suppress_warnings, proxies=proxies)
        self.data = DataClient(api_key, site, suppress_warnings=suppress_warnings, proxies=proxies)
        self.data_views = DataViewsClient(api_key, site, suppress_warnings=suppress_warnings, proxies=proxies)

    def __repr__(self):
        return "['models', 'search', 'data', 'data_views']"
