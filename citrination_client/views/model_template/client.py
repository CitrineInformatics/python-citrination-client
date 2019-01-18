import json

from citrination_client.base import BaseClient


class ModelTemplateClient(BaseClient):
    """
    Model template client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["validate"]
        super(ModelTemplateClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

    def validate(self, ml_template):
        """
        Runs the template against the validation endpoint, returns a message indicating status of the templte

        :param ml_template: Template to validate
        :return: OK or error message if validation failed
        """

        data = {
            "ml_template":
                ml_template
        }

        failure_message = "ML template validation invoke failed"

        res = self._get_success_json(self._post_json(
            'ml_templates/validate', data, failure_message=failure_message))['data']
        if res['valid']:
            return 'OK'
        return res['reason']
