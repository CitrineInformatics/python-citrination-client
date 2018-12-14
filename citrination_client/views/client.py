from citrination_client import BaseClient


class DataViewsClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "status", "predict", "design"]
        super(DataViewsClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

    def create(self, ml_template, search_template):
        pass
