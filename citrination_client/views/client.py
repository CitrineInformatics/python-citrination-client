

from citrination_client import BaseClient


class DataViewsClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False, proxies=None):
        members = ["create", "update", "delete", "get", "check_predict_status", "predict", "design"]
        super(DataViewsClient, self).__init__(api_key, webserver_host, members, suppress_warnings, proxies)

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
        print result
        return result['id']

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

        self._delete('data_views/' + id, None, failure_message=failure_message)

    def get(self, id):
        """
        Gets basic information about a view

        :param id: Identifier of the data view
        :return: Metadata about the view as JSON
        """

        failure_message = "Dataview get failed"
        return self._get_success_json(self._get(
            'v1/data_views/' + id, None, failure_message=failure_message))

    def create_ml_configuration(self, searchTemplate, extractAsKeys):
        """
        This method will spawn a server job to create a default ML configuration based on a search template and
        the extract as keys.

        :param searchTemplate: A search template defining the query (properties, datasets etc)
        :param extractAsKeys: Array of extract-as keys defining the descriptors
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """

        data = {
            "search_template":
                searchTemplate,
            "extract-as-keys":
                extractAsKeys
        }

        failure_message = "Configuration creation failed"
        return self._get_success_json(self._post_json(
            'v1/data_views/builders/simple/default', data, failure_message=failure_message))['id']

    def get_ml_configuration_status(self, jobId):
        """
        After invoking the create_ml_configuration async method, you can use this method to
        check on the status of the builder job.

        :param jobId: The identifier returned from create_ml_configuration
        :return: Job status
        """

        failure_message = "Get status on ml configuration failed"
        return self._get_success_json(self._get(
            'v1/data_views/builders/simple/default/' + jobId, None, failure_message=failure_message))

    def predict(self, dataViewId, predictionSource, usePrior, candidates):
        """
        Submits an async prediction request.

        :param dataViewId: The id returned from create
        :param predictionSource: 'scalar' or 'from_distribution'
        :param usePrior: True to use prior prediction, otherwise False
        :param candidates: Array of candidates
        :return: Predict request Id (used to check status)
        """

        data = {
            "predictionSource" :
                predictionSource,
            "usePrior" :
                usePrior,
            "candidates" :
                candidates
        }

        failure_message = "Configuration creation failed"
        return self._get_success_json(self._post_json(
            'v1/data_views/'+dataViewId+'/predict/submit', data, failure_message=failure_message))['uid']

    def check_predict_status(self, viewId, predictRequestId):
        """
        Returns a string indicating the status of the prediction job

        :param viewId: The id returned from data view create
        :param predictRequestId: The id returned from predict
        :return: String indicating state of the job (e.g. "running")
        """

        failure_message = "Get status on predict failed"
        return self._get_success_json(self._get(
            'v1/data_views/'+viewId+'/predict/'+predictRequestId+'/status',
            None, failure_message=failure_message))['status']

    def get_predict_result(self, viewId, predictRequestId):
        """
        Returns a string indicating the status of the prediction job

        :param viewId: The id returned from data view create
        :param predictRequestId: The id returned from predict
        :return: Array of candidates
        """

        failure_message = "Get results on predict failed"
        return self._get_success_json(self._get(
            'v1/data_views/' + viewId + '/predict/' + predictRequestId + '/results',
            None, failure_message=failure_message))['candidates']
