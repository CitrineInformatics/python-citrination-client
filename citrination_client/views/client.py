import json
import time

from citrination_client.models.client import ModelsClient

from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.model_report import ModelReport
from citrination_client.views.search_template.client import SearchTemplateClient

from citrination_client import BaseClient, DataViewStatus, ServiceStatus


class DataViewsClient(BaseClient):
    """
    Data Views client.
    """

    def __init__(self, api_key, site="https://citrination.com", suppress_warnings=False, proxies=None):
        """
        Contructor
        """
        members = [
            "create",
            "update",
            "delete",
            "get",
            "get_data_view_service_status",
            "create_ml_configuration_from_datasets",
            "create_ml_configuration",
            "get_model_reports",
            "get_relation_graph",
            "models",
            "search_template_client"
        ]
        super(DataViewsClient, self).__init__(api_key, site, members, suppress_warnings, proxies)

        self.models = ModelsClient(api_key, site, suppress_warnings, proxies)
        self.search_template_client = SearchTemplateClient(
            api_key, site, suppress_warnings, proxies
        )

    def validate(self, configuration):
        """
        Sends a request to Citrination to run some basic tests on the configuration.

        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :return: A set of notes describing the results of the validation request
        """

        data = {
            "configuration":
                configuration
        }

        failure_message = "Dataview validation failed"

        result = self._get_success_json(self._post_json(
            'v1/data_views/builder-configuration/validate', data, failure_message=failure_message))

        return result['data']

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

    def update(self, id, configuration = None, name = None, description = None):
        """
        Updates an existing data view from the search template and ml template given

        :param id: Identifier for the data view.  This returned from the create method.
        :param configuration: Information to construct the data view from (eg descriptors, datasets etc)
        :param name: Name of the data view
        :param description: Description for the data view
        """

        data = {}
        if configuration is not None:
            data['configuration'] = configuration
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description

        failure_message = "Dataview update failed"

        self._patch_json(
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
            'v1/data_views/' + data_view_id, None, failure_message=failure_message
        ))['data']['data_view']

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
        if not isinstance(dataset_ids, list):
            dataset_ids = [dataset_ids]

        available_columns = self.search_template_client.get_available_columns(dataset_ids)

        # Create a search template from dataset ids
        search_template = self.search_template_client.create(dataset_ids, available_columns)
        return self.create_ml_configuration(search_template, available_columns, dataset_ids)

    def create_ml_configuration(self, search_template, extract_as_keys, dataset_ids):
        """
        This method will spawn a server job to create a default ML configuration based on a search template and
        the extract as keys.
        This function will submit the request to build, and wait for the configuration to finish before returning.

        :param search_template: A search template defining the query (properties, datasets etc)
        :param extract_as_keys: Array of extract-as keys defining the descriptors
        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An identifier used to request the status of the builder job (get_ml_configuration_status)
        """
        data = {
            "search_template":
                search_template,
            "extract_as_keys":
                extract_as_keys
        }

        failure_message = "ML Configuration creation failed"
        config_job_id = self._get_success_json(self._post_json(
            'v1/descriptors/builders/simple/default/trigger', data, failure_message=failure_message))['data'][
            'result']['uid']

        while True:
            config_status = self.__get_ml_configuration_status(config_job_id)
            print('Configuration status: ', config_status)
            if config_status['status'] == 'Finished':
                ml_config = self.__convert_response_to_configuration(config_status['result'], dataset_ids)
                return ml_config
            time.sleep(5)

    def get_model_reports(self, data_view_id):
        """
        Retrieves the model reports of a data view

        :param data_view_id: the id of the view to retrieve model reports from
        :type data_view_id: str
        :return: A list of model reports
        :rtype: list of class:`ModelReport`
        """
        response = self._get('v1/data_views/{}/model_reports'.format(data_view_id)).json()
        return list(map(lambda report: ModelReport(report), response['data']))

    def get_relation_graph(self, data_view_id):
        """
        Retrieves the relation graph of data views with ML configured, that can
        be passed into the ``plot`` function of ``dagre_py.core`` for visualization.

        A relation graph shows you how your inputs, outputs, and latent variables
        are linked by Citrination's machine learning models.

        :param data_view_id: the id of the view to retrieve relation graphs from
        :type data_view_id: str
        :return: A dict containing a list of nodes and edges
        :rtype: dict
        """
        response = self._get('v1/data_views/{}/relation-graph'.format(data_view_id)).json()
        return response['data']

    def __convert_response_to_configuration(self, result_blob, dataset_ids):
        """
        Utility function to turn the result object from the configuration builder endpoint into something that
        can be used directly as a configuration.

        :param result_blob: Nested dicts representing the possible descriptors
        :param dataset_ids: Array of dataset identifiers to make search template from
        :return: An object suitable to be used as a parameter to data view create
        """

        builder = DataViewBuilder()
        builder.dataset_ids(dataset_ids)
        for i, (k, v) in enumerate(result_blob['descriptors'].items()):
            try:
                descriptor = self.__snake_case(v[0])
                print(json.dumps(descriptor))
                descriptor['descriptor_key'] = k
                builder.add_raw_descriptor(descriptor)
            except IndexError:
                pass

        for i, (k, v) in enumerate(result_blob['types'].items()):
            builder.set_role(k, v.lower())

        return builder.build()

    def __snake_case(self, descriptor):
        """
        Utility method to convert camelcase to snake
        :param descriptor: The dictionary to convert
        """
        newdict = {}
        for i, (k, v) in enumerate(descriptor.items()):
            newkey = ""
            for j, c in enumerate(k):
                if c.isupper():
                    if len(newkey) != 0:
                        newkey += '_'
                    newkey += c.lower()
                else:
                    newkey += c
            newdict[newkey] = v

        return newdict

    def __get_ml_configuration_status(self, job_id):
        """
        After invoking the create_ml_configuration async method, you can use this method to
        check on the status of the builder job.

        :param job_id: The identifier returned from create_ml_configuration
        :return: Job status
        """

        failure_message = "Get status on ml configuration failed"
        response = self._get_success_json(self._get(
            'v1/descriptors/builders/simple/default/' + job_id + '/status', None, failure_message=failure_message))[
            'data']
        return response
