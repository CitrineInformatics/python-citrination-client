from citrination_client.client import CitrinationClient
from os import environ
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import random
import string

parent_client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
client = parent_client.data_management
# Append dataset name with random string because one user can't have more than
# one dataset with the same name
random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
dataset_name = "Tutorial dataset " + random_string
dataset_id = client.create_data_set(name=dataset_name, description="Dataset for tutorial", share=0)['id']
test_file_root = './citrination_client/data_management/tests/test_files/'

def get_test_file_hierarchy_count():
    test_dir = test_file_root
    return sum([len(files) for r, d, files in os.walk(test_dir)])

def test_upload_pif():
    pif = System()
    pif.id = 0

    with open("tmp.json", "w") as fp:
        dump(pif, fp)
    response = client.upload_file("tmp.json", dataset_id)
    assert response["message"] == "Upload is complete."

def test_file_listing():
    src_path = test_file_root + "keys_and_values.json"
    dest_path = "test_file_list.json"
    client.upload(dataset_id, src_path, dest_path)
    listed_files = client.list_files(dataset_id, dest_path)["files"]
    assert len(listed_files) == 1
    assert listed_files[0] == dest_path

def test_upload_directory():
    count_to_add = get_test_file_hierarchy_count()
    src_path = test_file_root
    dest_path = "test_directory_upload/"
    before_count = client.matched_file_count(dataset_id)
    client.upload(dataset_id, src_path, dest_path)
    after_count = client.matched_file_count(dataset_id)
    assert after_count == (before_count + count_to_add)