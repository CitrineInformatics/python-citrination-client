from citrination_client import CitrinationClient
from os import environ, path, listdir
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import pytest
import unittest

class TestClient():

    @classmethod
    def setup_class(self):
        self.client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        self.set_id = loads(self.client.create_data_set(name="Tutorial dataset", description="Dataset for tutorial", share=0).content.decode('utf-8'))['id']
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

    def test_move_file(self):
        src_path = self.test_file_root + "weird_extensions.woodle"
        target_move_path = "TARGET_MOVE_PATH.txt"
        self.client.upload_file(src_path, self.set_id)
        self.client.move(self.set_id, src_path, target_move_path)
        files_matching_target = self.client.list(self.set_id, target_move_path)["files"]
        files_matching_source = self.client.list(self.set_id, src_path)["files"]
        assert len(files_matching_source) == 0
        assert len(files_matching_target) == 1
        assert files_matching_target[0] == target_move_path

    def test_copy_file(self):
        src_path = self.test_file_root + "keys_and_values.json"
        dest_path = "COPY_TEST.json"
        copied_path = "COPIED.json"
        self.client.upload(self.set_id, src_path, dest_path)
        before_copy_file_count = self.client.matched_file_count(self.set_id)
        self.client.copy(self.set_id, dest_path, copied_path)
        after_copy_file_count = self.client.matched_file_count(self.set_id)
        matched_name_file_count = self.client.matched_file_count(self.set_id, copied_path)
        assert after_copy_file_count == (before_copy_file_count + 1)
        assert matched_name_file_count == 1

    def test_file_listing(self):
        src_path = self.test_file_root + "keys_and_values.json"
        dest_path = "test_file_list.json"
        self.client.upload(self.set_id, src_path, dest_path)
        listed_files = self.client.list(self.set_id, dest_path)["files"]
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
    def test_predict(self):
        inputs = [{"CHEMICAL_FORMULA": "AlCu"}, ]
        resp = self.client.predict("betterdensitydemo", inputs)
        prediction = resp['candidates'][0]['Density']
        assert abs(prediction[0] - 5.786) < 0.1
