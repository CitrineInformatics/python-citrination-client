from citrination_client import *
from citrination_client.base.errors import CitrinationServerErrorException
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import pypif
import random
import time
import string
import requests
import json

def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

parent_client = CitrinationClient(os.environ["CITRINATION_API_KEY"])
client = parent_client.data
# Append dataset name with random string because one user can't have more than
# one dataset with the same name
dataset_name = "Tutorial dataset " + random_string()
dataset_id = client.create_dataset(name=dataset_name, description="Dataset for tutorial").id
test_file_root = './citrination_client/data/tests/test_files/'

def random_dataset_name():
    return "PyCCTestDataset" + random_string()

def get_test_file_hierarchy_count():
    test_dir = test_file_root
    return sum([len(files) for r, d, files in os.walk(test_dir)])

def test_upload_pif():
    """
    Tests that a PIF can be created, serialized, uploaded
    then downloaded and deserialized
    """
    pif = System()
    pif.id = 0
    uid = random_string()
    pif.uid = uid

    with open("tmp.json", "w") as fp:
        dump(pif, fp)
    assert client.upload(dataset_id, "tmp.json").successful()
    tries = 0
    while True:
        try:
            pif = client.get_pif(dataset_id, uid)
            break
        except CitrinationServerErrorException:
            if tries < 10:
                tries += 1
                time.sleep(1)
            else:
                raise

    with open("tmp.json", "r") as fp:
        assert json.loads(fp.read())["uid"] == pif.uid

def test_dataset_version_bump():
    """
    Tests that create_dataset_version bumps the version
    number
    """
    dataset_name = random_dataset_name()
    dataset_id = client.create_dataset(name=dataset_name).id
    assert client.create_dataset_version(dataset_id).number == 2
    assert client.create_dataset_version(dataset_id).number == 3

def test_dataset_update():
    """
    Tests that dataset metadata can be updated successfully
    """
    dataset_name = random_dataset_name()
    dataset_id = client.create_dataset(name=dataset_name).id
    new_name = random_dataset_name()
    new_description = random_string()
    dataset = client.update_dataset(dataset_id, name=new_name, description=new_description)
    assert dataset.name == new_name
    assert dataset.description == new_description

    search_count = 0
    while search_count < 10:
        response = parent_client.dataset_search(DatasetReturningQuery(
                size=1,
                query=DataQuery(
                    dataset=DatasetQuery(
                        id=Filter(equal=dataset.id)))))
        if len(response.hits) > 0:
            break
        else:
            search_count += 1
        time.sleep(1)

    assert response.hits[0].name == new_name
    assert response.hits[0].description == new_description

def test_public_update():
    """
    Tests that requests to make a dataset public are
    successful
    """
    dataset_name = random_dataset_name()
    dataset_id = client.create_dataset(name=dataset_name).id
    # Just ensure no 500s until we can check permissions from here
    client.update_dataset(dataset_id, public=True)
    client.update_dataset(dataset_id, public=False)

def test_file_listing_and_url_retrieval():
    """
    Tests that files can be uploaded and then retrieved
    with presigned urls
    """
    src_path = test_file_root + "keys_and_values.json"
    dest_path = "test_file_list.json"
    assert client.upload(dataset_id, src_path, dest_path).successful()
    listed_files = client.list_files(dataset_id, dest_path)
    assert len(listed_files) == 1
    assert listed_files[0] == dest_path
    dataset_file = client.get_dataset_file(dataset_id, dest_path)
    assert dataset_file.path == dest_path
    assert requests.get(dataset_file.url).status_code == 200

def test_upload_directory():
    """
    Tests that if a path to a directory is given to
    `upload`, all the files get recursively uploaded
    """
    count_to_add = get_test_file_hierarchy_count()
    src_path = test_file_root
    dest_path = "test_directory_upload/"
    before_count = client.matched_file_count(dataset_id)
    assert client.upload(dataset_id, src_path, dest_path).successful()
    revolver_count = client.matched_file_count(dataset_id, "test_directory_upload/revolver")
    assert client.matched_file_count(dataset_id, "weird_extensions.woodle") == 1
    assert revolver_count == 3
    after_total_count = client.matched_file_count(dataset_id)
    assert after_total_count == (before_count + count_to_add)