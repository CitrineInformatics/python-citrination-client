import json
import requests_mock
import os
import time
import uuid

from citrination_client import CitrinationClient

from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.search_template.client import SearchTemplateClient

from citrination_client.views.client import DataViewsClient


def load_file_as_json(path):
    """
    Given a filepath, loads the file as a dictionary from JSON

    :param path: The path to a JSON file
    """
    with open(path, "r") as f:
        parsed_dict = json.load(f)
    return parsed_dict


def test_workflow():
    print('Starting data view creation workflow')

    site = "https://citrination.com"
    search_template_client = SearchTemplateClient(os.environ["CITRINATION_API_KEY"], site)
    data_views_client = DataViewsClient(os.environ["CITRINATION_API_KEY"], site)

    search_template_url = "{}/api/v1/search_templates{}"
    datasets_url = "{}/api/v1/datasets{}"
    data_view_url = "{}/api/v1/data_views{}"
    descriptors_url = "{}/v1/descriptors{}"

    with requests_mock.Mocker() as m:
        # Setup mocks
        m.post(
            search_template_url.format(site, '/builders/from-dataset-ids'),
            json=dict(data=load_file_as_json('./citrination_client/views/tests/test_search_template.json'))
        )

        m.post(
            search_template_url.format(site, '/prune-to-extract-as'),
            json=dict(data=load_file_as_json('./citrination_client/views/tests/test_search_template.json'))
        )

        m.post(
            datasets_url.format(site, '/get-available-columns'),
            json=dict(data=load_file_as_json('./citrination_client/views/tests/available_columns.json'))
        )

        m.post(
            descriptors_url.format(site, '/trigger-job'),
            json=dict(data=dict(poll_url=descriptors_url.format(site, '/job-status/1234')))
        )

        m.post(
            descriptors_url.format(site, '/job-status'),
            json=dict(data=load_file_as_json('./citrination_client/views/tests/column_descriptors.json'))
        )

        m.post(
            data_view_url.format(site, ''),
            json=dict(data=dict(id=555))
        )

        # Get available columns
        available_columns = search_template_client.get_available_columns([1234])
        assert len(available_columns) == 524

        # Create a search template from dataset ids
        search_template = search_template_client.create([1234], available_columns)
        assert search_template['query'][0]['system'][0]['tags'][0]['category'] == 'General'

        # Create ML configuration
        dv_builder = DataViewBuilder()
        dv_builder.add_real_descriptor('Property Melting point', 'Output', 'Infinity', '0')
        dv_builder.add_organic_descriptor('Property SMILES', 'Input')
        dv_config = dv_builder.build()

        # Create an ML template
        data_view_id = data_views_client.create(dv_config, "my view", "my description")
        assert data_view_id == 555


def test():
    site = "https://stage.citrination.com"
    client = CitrinationClient(os.environ["CITRINATION_API_KEY"], site)
    data_views_client = client.data_views

    # Create ML configuration
    print('Build ML config')
    dv_builder = DataViewBuilder()
    dv_builder.set_dataset_ids(['29'])
    dv_builder.set_group_by(['SMILES'])
    dv_builder.add_real_descriptor(u'Property $\\varepsilon$$_{gap}$ ($\\varepsilon$$_{LUMO}$-$\\varepsilon$$_{HOMO}$)',
                                   'Infinity', '0', 'output')
    dv_builder.add_organic_descriptor('SMILES', 'input')
    dv_config = dv_builder.build()

    # Create the data view
    view_name = 'pycc view ' + str(uuid.uuid4())
    print('Create data view: ' + view_name)
    data_view_id = data_views_client.create(dv_config, view_name, 'a test view created by pycc')

    view_metadata = data_views_client.get(data_view_id)
    print('View metadata: ' + str(view_metadata))
    print('Data view id:' + str(data_view_id))

    data_views_client.retrain(data_view_id)

    while True:
        status = data_views_client.get_data_view_service_status(data_view_id)
        print('Data view status: ' + status.predict.reason)
        if status.predict.is_ready():
            break
        time.sleep(5)

    # print 'Test update'
    # data_views_client.update(data_view_id, dv_config, view_name+'-upd', 'updated description from pycc')

    print('Submitting a predict request')
    predict_id = data_views_client.submit_predict_request(data_view_id,
                                                          [{
                                                              u'Property $\\varepsilon$$_{gap}$ ($\\varepsilon$$_{LUMO}$-$\\varepsilon$$_{HOMO}$)': 'float'},
                                                              {"SMILES": 'CCC'}], 'scalar', False)
    print('Predict ID: ' + predict_id)

    while True:
        predict_status = data_views_client.check_predict_status(data_view_id, predict_id)
        print('Prediction job status: ' + predict_status['status'])
        if predict_status['status'] == 'Finished':
            break
        time.sleep(5)

    predict_result = predict_status['results']

    print('Prediction results: ' + json.dumps(predict_result))
    data_views_client.delete(data_view_id)
