import json

import requests_mock

import os

from citrination_client.views.search_template.client import SearchTemplateClient

from citrination_client.views.model_template.client import ModelTemplateClient

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
    model_template_client = ModelTemplateClient(os.environ["CITRINATION_API_KEY"], site)
    data_views_client = DataViewsClient(os.environ["CITRINATION_API_KEY"], site)

    search_template_url = "{}/api/search_templates{}"
    datasets_url = "{}/api/datasets{}"
    machine_learning_url = "{}/api/ml_templates{}"
    data_view_url = "{}/api/data_views{}"

    ml_config = {
        "Property Melting point": {
            "role": "Output",
            "descriptor": {
                "category": "Real",
                "upperBound": "Infinity",
                "lowerBound": "0"
            }
        },
        "Property SMILES": {
            "role": "Input",
            "descriptor": {
                "category": "Organic"
            }
        }
    }

    with requests_mock.Mocker() as m:
        # Setup mocks
        m.post(
            search_template_url.format(site, '/from-dataset-ids'),
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
            machine_learning_url.format(site, ''),
            json=dict(data=load_file_as_json('./citrination_client/views/tests/ml_template.json'))
        )

        m.post(
            machine_learning_url.format(site, '/validate'),
            json=dict(data=dict(valid=True, reason="OK"))
        )

        m.post(
            data_view_url.format(site, ''),
            json=dict(id=555)
        )

        # Get available columns
        available_columns = search_template_client.get_available_columns([1234])
        assert len(available_columns) == 524

        # Create a search template from dataset ids
        search_template = search_template_client.create_with_extract_as_keys([1234], available_columns)
        assert search_template['query'][0]['system'][0]['tags'][0]['category'] == 'General'

        # Create an ML template
        ml_template = model_template_client.create(search_template, ml_config)
        assert ml_template['descriptors'][0]['category'] == 'Real'

        # Validate the template
        result = model_template_client.validate(ml_template)
        assert result == "OK"

        # Create the dataview
        data_view_id = data_views_client.create(search_template, ml_template, available_columns,
                                                [1234], 'my view', 'a test view created by pycc')
        assert data_view_id == 555

