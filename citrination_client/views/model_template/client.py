from citrination_client.base import BaseClient


class ModelTemplateClient(BaseClient):
    """
    Model template client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["validate"]
        super(ModelTemplateClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)
