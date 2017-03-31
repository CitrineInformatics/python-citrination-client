from citrination_client import CitrinationClient
from os import environ, path, listdir
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import pytest
import random
import string
import unittest

class TestClient():

    @classmethod
    def setup_class(self):
        self.client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        # Append dataset name with random string because one user can't have more than
        # one dataset with the same name
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        dataset_name = "Tutorial dataset " + random_string
        self.set_id = loads(self.client.create_data_set(name=dataset_name, description="Dataset for tutorial", share=0).content.decode('utf-8'))['id']
        self.test_file_root = './citrination_client/tests/test_files/'

    def get_test_file_hierarchy_count(self):
        test_dir = self.test_file_root
        return sum([len(files) for r, d, files in os.walk(test_dir)])

    def test_start_client(self):
        assert self.client is not None

    def test_upload_pif(self):
        pif = System()
        pif.id = 0

        with open("tmp.json", "w") as fp:
            dump(pif, fp)
        response = loads(self.client.upload_file("tmp.json", self.set_id))
        assert response["message"] == "Upload is complete."

    def test_file_listing(self):
        src_path = self.test_file_root + "keys_and_values.json"
        dest_path = "test_file_list.json"
        self.client.upload(self.set_id, src_path, dest_path)
        listed_files = self.client.list_files(self.set_id, dest_path)["files"]
        assert len(listed_files) == 1
        assert listed_files[0] == dest_path

    def test_upload_directory(self):
        count_to_add = self.get_test_file_hierarchy_count()
        src_path = self.test_file_root
        dest_path = "test_directory_upload/"
        before_count = self.client.matched_file_count(self.set_id)
        self.client.upload(self.set_id, src_path, dest_path)
        after_count = self.client.matched_file_count(self.set_id)
        assert after_count == (before_count + count_to_add)

    @pytest.mark.skipif(True, reason="Depends on model that user doesn't always have access to")
    def test_predict():
        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        inputs = [{"CHEMICAL_FORMULA": "AlCu"}, ]
        resp = client.predict("betterdensitydemo", inputs)
        prediction = resp['candidates'][0]['Density']
        assert abs(prediction[0] - 5.786) < 0.1


    @pytest.mark.skipif(True, reason="Depends on model that user doesn't always have access to")
    def test_predict_custom():
        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        input = {"canary_x": "0.5", "temperature": "100", "canary_y": "0.75"}
        resp = client.predict_custom("canary", input)
        prediction = resp['candidates'][0]
        assert 'canary_zz' in prediction.keys()
        assert 'canary_z' in prediction.keys()