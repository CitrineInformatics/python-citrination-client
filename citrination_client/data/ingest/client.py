from citrination_client import BaseClient
from citrination_client.data.ingest import IngesterList
from citrination_client.data.ingest import Ingester

class IngestClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, site="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["list_ingesters", "submit"]
        super(IngestClient, self).__init__(
            api_key, site, members, suppress_warnings, proxies
        )

    def logs(self, file_id):
        """
        Retrieves ingestion logs for the given file id

        :return 404 or Presigned URL to retrieve ingest logs
        """

        response = self._get_success_json(
            self._get('v1/ingest/logs/{}'.format(file_id),
                      failure_message='No logs available for {} or file does not exist'.format(file_id))
        )
        return response["data"]


    def list_ingesters(self):
        """
        Retrieves the list of available ingesters

        :return: The list of ingesters available for ingestion
        :rtype: :class:`IngesterList`
        """
        response = self._get_success_json(
            self._get(
                'v1/ingest/list_ingesters',
                failure_message='Failed to retrieve available ingesters'
            ),
        )['ingesters']

        return IngesterList(response)

    def submit(self, dataset_id, file_path, ingester, arguments = []):
        """
        Submits an ingest request using a custom (non-default) ingester

        :param dataset_id: The dataset being uploaded to
        :type dataset_id: str
        :param file_path: The destination path of the file
        :type file_path: str
        :param ingester: The ingester being used
        :type ingester: class:`citrination_client.data.ingest.Ingester`
        :param arguments: ingester arguments (optional), arguments should
                          contain keys "name" and "value"
        :type arguments: list of dict
        """
        ingester_with_values = self._apply_ingester_arguments(
            ingester, arguments
        )
        data = {
            "ingester": ingester_with_values.as_json(),
            "dataset_id": dataset_id,
            "target_path": file_path
        }

        self._get_success_json(
            self._post_json(
                'v1/ingest/submit',
                data,
                failure_message='Failed to submit ingestion request'
            )
        )

    def validate_ingester(self, ingester, arguments = []):
        """
        Validates that the ingester and argument values are valid.

        :param ingester: The ingester being used
        :type ingester: class:`citrination_client.data.ingest.Ingester`
        :param arguments: ingester arguments (optional), arguments should
                          contain keys "name" and "value"
        :type arguments: list of dict
        """
        ingester_with_values = self._apply_ingester_arguments(ingester, arguments)
        self._get_success_json(
            self._post_json(
                'v1/ingest/validate_ingester',
                { "ingester": ingester_with_values.as_json() },
                failure_message='Failed to submit ingestion request'
            )
        )

    def _apply_ingester_arguments(self, ingester, arguments = []):
        """
        Validates that the ingester and arguments passed to the #submit method
        are valid, and applies those arguments to a copy of the ingester.

        :param ingester: The ingester being used
        :type ingester: class:`citrination_client.data.ingest.Ingester`
        :param arguments: ingester arguments (optional), arguments should
                          contain keys "name" and "value"
        :type arguments: list of dict
        :return: a copy of the ingester with the argument values applied
        :rtype: citrination_client.data.ingest.Ingester
        """
        if not isinstance(ingester, Ingester):
            raise TypeError(
                "Expected ingester to be an instance of Ingester, received {}".format(
                    ingester.__class__
                )
            )
        else:
            self._validate_arguments_shape(arguments)

        ingester_copy = ingester.clone()

        for argument in arguments:
            ingester_copy.find_argument(argument['name'])['value'] = argument['value']

        return ingester_copy

    def _validate_arguments_shape(self, arguments):
        """
        Validates the shape of the arguments passed into _apply_ingester_arguments -
        that they are an array of dicts containing 'name' and 'value' keys

        :param arguments: ingester arguments (optional), arguments should
                          contain keys "name" and "value"
        :type arguments: list of dict
        """
        if not isinstance(arguments, list):
            raise TypeError(
                "Expected arguments to be an instance of list, received {}".format(
                    arguments.__class__
                )
            )
        else:
            improper_arguments = list(
                filter(
                    lambda arg: (
                        not isinstance(arg, dict) or
                        not 'name' in arg or
                        not 'value' in arg
                    ),
                    arguments
                )
            )
            if len(improper_arguments) > 0:
                raise TypeError(
                    "Expected all arguments to be dictionaries containing " \
                    "'name' and 'value' keys"
                )
