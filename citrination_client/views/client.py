import json

from citrination_client import BaseClient


class DataViewsClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "status", "predict", "design"]
        super(DataViewsClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

    def create(self, search_template, ml_template, name, description):
        """
        Creates a data view from the search template and ml template given

        :param search_template: Search template to build data view from
        :param ml_template: ML template to build data view from
        :param name: Name of the data view
        :param description: Description for the data view
        :return: The data view id
        """

        data = {
            "search_template":
                search_template,
            "ml_template":
                ml_template,
            "name":
                name,
            "description":
                description
        }

        failure_message = "Dataview creation failed"

        return self._get_success_json(self._post_json(
            'data_views', data, failure_message=failure_message))['id']