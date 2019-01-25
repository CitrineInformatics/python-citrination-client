import time

from citrination_client.views.search_template.client import SearchTemplateClient

from citrination_client import BaseClient, DataViewStatus, ServiceStatus


class DataViewsClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "update", "delete", "get", "check_predict_status", "submit_predict_request",
                   "get_predict_result"]
        super(DataViewsClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)
        self.search_template_client = SearchTemplateClient(api_key, webserver_host)

    def create(self, configuration, name, description):
        """
        Creates a data view from the search template and ml template given

        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :param name: Name of the data view
        :param description: Description for the data view
        :return: The data view id
        """

        data = {
            "configuration":
                configuration,
            "name":
                name,
            "description":
                description
        }

        failure_message = "Dataview creation failed"

        result = self._get_success_json(self._post_json(
            'v1/data_views', data, failure_message=failure_message))
        data_view_id = result['data']['id']

        return data_view_id

    def update(self, id, configuration, name, description):
        """
        Updates an existing data view from the search template and ml template given

        :param id: Identifier for the data view.  This returned from the create method.
        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :param name: Name of the data view
        :param description: Description for the data view
        """

        data = {
            "configuration":
                configuration,
            "name":
                name,
            "description":
                description
        }

        failure_message = "Dataview creation failed"

        self._put_json(
            'v1/data_views/' + id, data, failure_message=failure_message)

    def delete(self, id):
        """
        Deletes a data view.

        :param id: Identifier of the data view
        """

        failure_message = "Dataview delete failed"

        self._delete('v1/data_views/' + id, None, failure_message=failure_message)

    def get(self, data_view_id):
        """
        Gets basic information about a view

        :param data_view_id: Identifier of the data view
        :return: Metadata about the view as JSON
        """

        failure_message = "Dataview get failed"
        return self._get_success_json(self._get(
            'v1/data_views/' + data_view_id, None, failure_message=failure_message))['data']['data_view']

    def get_data_view_service_status(self, data_view_id):
        """
        Retrieves the status for all of the services associated with a data view:
            - predict
            - experimental_design
            - data_reports
            - model_reports

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :return: A :class:`DataViewStatus`
        :rtype: DataViewStatus
        """

        url = "data_views/{}/status".format(data_view_id)

        response = self._get(url).json()
        result = response["data"]["status"]

        return DataViewStatus(
            predict=ServiceStatus.from_response_dict(result["predict"]),
            experimental_design=ServiceStatus.from_response_dict(result["experimental_design"]),
            data_reports=ServiceStatus.from_response_dict(result["data_reports"]),
            model_reports=ServiceStatus.from_response_dict(result["model_reports"])
        )

    def create_ml_configuration_from_datasets(self, dataset_ids):
        """
        Creates an ml configuration from dataset_ids and extract_as_keys

        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """
        available_columns = self.search_template_client.get_available_columns(dataset_ids)

        # Create a search template from dataset ids
        search_template = self.search_template_client.create([29], available_columns)
        return self.create_ml_configuration(search_template,available_columns)

    def create_ml_configuration(self, search_template, extract_as_keys):
        """
        This method will spawn a server job to create a default ML configuration based on a search template and
        the extract as keys.

        :param search_template: A search template defining the query (properties, datasets etc)
        :param extract_as_keys: Array of extract-as keys defining the descriptors
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """

        data = {
            "search_template":
                search_template,
            "extract-as-keys":
                extract_as_keys
        }

        failure_message = "Configuration creation failed"
        return self._get_success_json(self._post_json(
            'v1/data_views/builders/simple/default', data, failure_message=failure_message))['id']

    def __get_ml_configuration_status(self, job_id):
        """
        After invoking the create_ml_configuration async method, you can use this method to
        check on the status of the builder job.

        :param job_od: The identifier returned from create_ml_configuration
        :return: Job status
        """

        failure_message = "Get status on ml configuration failed"
        return self._get_success_json(self._get(
            'v1/data_views/builders/simple/default/' + job_id, None, failure_message=failure_message))

    def retrain(self, dataview_id):
        """
        Start a model retraining
        :param dataview_id: The ID of the views
        :return:
        """
        url = 'data_views/{}/retrain'.format(dataview_id)
        response = self._post_json(url, data={})
        if response.status_code != 200:
            raise RuntimeError('Retrain requested ' + str(response.status_code) + ' response: ' + str(response.message))
        return True

    def submit_predict_request(self, data_view_id, candidates, prediction_source='scalar', use_prior=True ):
        """
        Submits an async prediction request.

        :param data_view_id: The id returned from create
        :param candidates: Array of candidates
        :param prediction_source: 'scalar' or 'from_distribution'
        :param use_prior: True to use prior prediction, otherwise False
        :return: Predict request Id (used to check status)
        """

        data = {
            "prediction_source":
                prediction_source,
            "use_prior":
                use_prior,
            "candidates":
                candidates
        }

        failure_message = "Configuration creation failed"
        return self._get_success_json(self._post_json(
            'v1/data_views/' + str(data_view_id) + '/predict/submit', data, failure_message=failure_message))['data']['uid']

    def check_predict_status(self, view_id, predict_request_id):
        """
        Returns a string indicating the status of the prediction job

        :param view_id: The data view id returned from data view create
        :param predict_request_id: The id returned from predict
        :return: Status data, also includes results if state is finished
        """

        failure_message = "Get status on predict failed"
        return self._get_success_json(self._get(
            'v1/data_views/' + view_id + '/predict/' + predict_request_id + '/status',
            None, failure_message=failure_message))['data']
