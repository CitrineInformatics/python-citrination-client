from citrination_client.base import BaseClient


class ModelTemplateClient(BaseClient):
    """
    Model template client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "validate"]
        super(ModelTemplateClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

    def create(self, search_template, ml_config):
        """
        Creates a machine learning template from a search template and an ml config

        :param search_template: Search template to make ML template from
        :param ml_config: Machine learning configuration
        :return: New ML template based on the search template and config
        """

        data = {
            "search_template":
                search_template,
            "ml_config":
                ml_config
        }

        failure_message = "Failed to create ml template"

        return self._get_success_json(self._post_json(
            'ml_templates', data, failure_message=failure_message))['data']

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
