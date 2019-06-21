import json
import os

import requests_mock

from citrination_client.views.client import DataViewsClient
from citrination_client.views.data_view_builder import DataViewBuilder
from citrination_client.views.descriptors import *
from citrination_client.views.search_template.client import SearchTemplateClient


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

    site = os.environ["CITRINATION_SITE"]
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

        m.patch(
            data_view_url.format(site, '/555'),
            json=dict()
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
        desc = RealDescriptor('Property Melting point', '-10000000000', '0')
        dv_builder.add_descriptor(desc, 'Output')
        desc = OrganicDescriptor('Property SMILES')
        dv_builder.add_descriptor(desc, 'Input')
        dv_config = dv_builder.build()

        # Create an ML template
        data_view_id = data_views_client.create(dv_config, "my view", "my description")
        assert data_view_id == 555

        # Update an ML template
        data_views_client.update("555", dv_config, "my view", "my description")


def test_workflow_blocking():
    site = os.environ["CITRINATION_SITE"]
    search_template_client = SearchTemplateClient(os.environ["CITRINATION_API_KEY"], site)
    data_views_client = DataViewsClient(os.environ["CITRINATION_API_KEY"], site)

    search_template_url = "{}/api/v1/search_templates{}"
    datasets_url = "{}/api/v1/datasets{}"
    data_view_url = "{}/api/v1/data_views{}"
    descriptors_url = "{}/v1/descriptors{}"
    ready_iter = iter([0,1]*10)
    prog_iter = iter([0,1]*10)

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

        m.get(
            site + '/api/data_views/555/status',
            json={
                    "data":{
                        "status":{
                            "predict":{
                                "reason": "Please wait for machine learning features to become available",
                                "ready": next(ready_iter),
                                "context": "notice",
                                "event": {
                                    "title": "Initializing machine learning services",
                                    "subtitle": "Doin some other stuff",
                                    "normalizedProgress": next(prog_iter)
                                }
                            },
                            "experimental_design":{
                                "ready":True,
                                "reason": None,
                                "context": None
                            },
                            "data_reports":{
                                "ready":True,
                                "reason": None,
                                "context": None
                            },
                            "model_reports":{
                                "ready":True,
                                "reason": None,
                                "context": None
                            }
                        }
                    }
                }
        )

        m.patch(
            data_view_url.format(site, '/555'),
            json=dict()
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
        desc = RealDescriptor('Property Melting point', '-10000000000', '0')
        dv_builder.add_descriptor(desc, 'Output')
        desc = OrganicDescriptor('Property SMILES')
        dv_builder.add_descriptor(desc, 'Input')
        dv_config = dv_builder.build()

        # Create an ML template
        data_view_id = data_views_client.create(dv_config, "my view", "my description", block_until_complete=True)
        assert data_view_id == 555

        # Update an ML template
        data_views_client.update("555", dv_config, "my view", "my description", block_until_complete=True)


def test_descriptor():
    print('Testing descriptor')
    dv_builder = DataViewBuilder()

    desc = RealDescriptor('Property 1', lower_bound=-100000, upper_bound=1000000)
    dv_builder.add_descriptor(desc, 'input')

    desc = AlloyCompositionDescriptor('Property 2', 'Al')
    dv_builder.add_descriptor(desc, 'input')

    desc = OrganicDescriptor('Property 3')
    dv_builder.add_descriptor(desc, 'input')

    desc = InorganicDescriptor('Property 4', 5)
    dv_builder.add_descriptor(desc, 'input')

    desc = CategoricalDescriptor('Property 5', ['Category A', 'Category B'])
    dv_builder.add_descriptor(desc, 'input')

    desc = IntDescriptor('Property 6', lower_bound=0, upper_bound=100)
    dv_builder.add_descriptor(desc, 'input')

    config = dv_builder.build()
    json.dumps(config)
