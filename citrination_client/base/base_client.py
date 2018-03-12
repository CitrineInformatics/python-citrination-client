import requests
import json
from citrination_client.util.quote_finder import quote
from errors import *

class BaseClient(object):
    """
    Base class that holds the universal constructor, utilities, etc
    """

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        """
        Constructor.

        :param webserver_host: local pointer to the tunnel to the cmc web host.
        """
        self.headers = {
            'X-API-Key': quote(api_key),
            'Content-Type': 'application/json',
            'X-Citrination-API-Version': '1.0.0'
        }
        self.api_url = webserver_host + '/api'

    # ==== Private Utilities ===

    def __get_qualified_route(self, route):
        """
        Get a fully qualified api route.
        :param route: the route (e.g., /model)
        :return: the fully qualified route (e.g., https://citrination.com/model)
        """
        return "{}/{}".format(self.api_url, route)

    def _get_headers(self, headers=None):
        if headers:
            headers = headers
        else:
            headers = self.headers
        return headers

    def _get(self, route, headers=None):
        """
        Execute a post request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        result = requests.get(self.__get_qualified_route(route), headers=headers, verify=False)
        return self._check_response_for_version_mismatch(result)

    def _post_json(self, route, data, headers=None):
        return self._post(route, json.dumps(data), headers)

    def _post(self, route, data, headers=None):
        """
        Execute a post request and return the result
        :param data:
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        print(self.__get_qualified_route(route))
        result = requests.post(self.__get_qualified_route(route), headers=headers, data=data)
        return self._check_response_for_version_mismatch(result)

    def _put_json(self, route, data, headers=None):
        return self._put(route, json.dumps(data), headers)

    def _put(self, route, data, headers=None):
        """
        Execute a put request and return the result
        :param data:
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        result = requests.put(self.__get_qualified_route(route), headers=headers, data=data,
             verify=False)
        return self._check_response_for_version_mismatch(result)

    def _delete(self, route, headers=None):
        """
        Execute a delete request and return the result
        :param headers:
        :return:
        """
        headers = self._get_headers(headers)
        result = requests.delete(self.__get_qualified_route(route), headers=headers, verify=False)
        return self._check_response_for_version_mismatch(result)

    def _check_response_for_version_mismatch(self, response):
        try:
            response_content = response.json()
        except ValueError:
            print("Received unparseable JSON: {}, {}".format(response.status_code, response.content))
            raise
        try:
            if response.status_code == 400:
                error_type = response_content["error_type"]
                if error_type == "Version Mismatch":
                    raise APIVersionMismatchException("Version mismatch with Citrination identified. Please check for available PyCC updates")
            return response
        except KeyError:
            return response