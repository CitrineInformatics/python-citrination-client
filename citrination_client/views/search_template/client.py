from citrination_client import BaseClient


class SearchTemplateClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "get_available_columns"]
        super(SearchTemplateClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

    def create(self, ml_template, search_template):
        pass
