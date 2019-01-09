import json

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

    def get_available_columns(self, dataset_ids):
        """
        Retrieves the set of columns from the combination of dataset ids given

        :param dataset_ids: The id of the dataset to retrieve columns from
        :type dataset_ids: list of int
        :return: A list of column names from the dataset ids given.
        :rtype: list of str
        """

        data = {
            "dataset_ids":
                dataset_ids
        }

        failure_message = "Failed to get available columns in dataset(s) {}".format(dataset_ids)

        return self._get_success_json(self._post_json(
            'datasets/get-available-columns', data, failure_message=failure_message))['data']

    def generate_search_template(self, dataset_ids):
        """
        Generates a default search templates from the available columns in the dataset ids given.

        :param dataset_ids: The id of the dataset to retrieve files from
        :type dataset_ids: list of int
        :return: A search template based on the columns in the datasets given
        """

        data = {
            "dataset_ids":
                dataset_ids
        }

        failure_message = "Failed to generate a search template from columns in dataset(s) {}".format(dataset_ids)

        return self._get_success_json(self._post_json(
            'search_templates/from-dataset-ids', data, failure_message=failure_message))['data']

    def prune_search_template(self, extract_as_keys, search_template):
        """
        Returns a new search template, but the new template has only the extract_as_keys given.

        :param extract_as_keys: List of extract as keys to keep
        :param search_template: The search template to prune
        :return: New search template with pruned columns
        """

        data = {
            "extract_as_keys":
                extract_as_keys,
            "search_template":
                search_template
        }

        failure_message = "Failed to prune a search template"

        return self._get_success_json(self._post_json(
            'search_templates/prune-to-extract-as', data, failure_message=failure_message))['data']

    def create_machine_learning_template(self, search_template, ml_config):
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

    def validate_machine_learning_template(self, ml_template):
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


    def create_data_view(self, search_template, ml_template, selected_columns, dataset_ids, name, description):
        """
        Creates a data view from the search template and ml template given

        :param search_template: Search template to build data view from
        :param ml_template: ML template to build data view from
        :param selected_columns: List of columns (see get_available_columns) for the data view
        :param dataset_ids: List of datasets to use in the data view
        :param name: Name of the data view
        :param description: Description for the data view
        :return: The data view id
        """

        data = {
            "search_template":
                search_template,
            "ml_template":
                ml_template,
            "selected_columns":
                selected_columns,
            "dataset_ids":
                dataset_ids,
            "name":
                name,
            "description":
                description
        }

        failure_message = "Dataview creation failed"

        return self._get_success_json(self._post_json(
            'data_views', data, failure_message=failure_message))['id']