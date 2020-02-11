from citrination_client import BaseClient


class SearchTemplateClient(BaseClient):
    """
    Search Template client.
    """

    def __init__(self, api_key, site="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "get_available_columns"]
        super(SearchTemplateClient, self).__init__(api_key, site, members, suppress_warnings, proxies)

    def create(self, dataset_ids, extract_as_keys):
        """
        Retrieves the set of columns from the combination of dataset ids given

        :param dataset_ids: The id of the dataset to retrieve columns from
        :type dataset_ids: list of int
        :param extract_as_keys: The list of property/condition/preparation step
                                names from the datasets that are to be included
                                in the search template
        :type extract_as_keys: list of str
        :return: New search template with pruned columns
        :rtype: dict
        """
        search_template = self.__generate_search_template(dataset_ids)
        return self.__prune_search_template(extract_as_keys, search_template)

    def get_available_columns(self, dataset_ids):
        """
        Retrieves the set of columns from the combination of dataset ids given

        :param dataset_ids: The id of the dataset to retrieve columns from
        :type dataset_ids: list of int
        :return: A list of column names from the dataset ids given.
        :rtype: list of str
        """
        if not isinstance(dataset_ids, list):
            dataset_ids = [dataset_ids]

        data = {
            "dataset_ids":
                dataset_ids
        }

        failure_message = "Failed to get available columns in dataset(s) {}".format(dataset_ids)

        return self._get_success_json(self._post_json(
            'v1/datasets/get-available-columns', data, failure_message=failure_message))['data']

    def __generate_search_template(self, dataset_ids):
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
            'v1/search_templates/builders/from-dataset-ids', data, failure_message=failure_message))['data']


    def __prune_search_template(self, extract_as_keys, search_template):
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
            'v1/search_templates/prune-to-extract-as', data, failure_message=failure_message))['data']
