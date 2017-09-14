from citrination_client import CitrinationClient
from os import environ
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import random
import string


def _almost_equal(test_value, reference_value, tolerance=1.0e-9):
    """
    Numerical equality with a tolerance
    """
    return abs(test_value - reference_value) < tolerance


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

    @staticmethod
    def _test_prediction_values(prediction):
        """
        Assertions for the test_predict and test_predict_distribution methods
        """
        egap = '$\\varepsilon$$_{gap}$ ($\\varepsilon$$_{LUMO}$-$\\varepsilon$$_{HOMO}$)'
        voltage = 'Open-circuit voltage (V$_{OC}$)'
        assert 'Mass'  in prediction, "Mass prediction missing (check ML logic)"
        assert egap    in prediction, "E_gap prediction missing (check ML logic)"
        assert voltage in prediction, "V_OC prediction missing (check ML logic)"
 
        assert _almost_equal(prediction['Mass'][0], 250,  60.0), "Mass mean prediction beyond tolerance (check ML logic)"
        assert _almost_equal(prediction['Mass'][1], 30.0, 40.0), "Mass sigma prediction beyond tolerance (check ML logic)"
        assert _almost_equal(prediction[egap][0], 2.6,  0.7), "E_gap mean prediction beyond tolerance (check ML logic)"
        assert _almost_equal(prediction[egap][1], 0.50, 0.55), "E_gap sigma prediction beyond tolerance (check ML logic)"
        assert _almost_equal(prediction[voltage][0], 1.0, 0.9), "V_OC mean prediction beyond tolerance (check ML logic)"
        assert _almost_equal(prediction[voltage][1], 0.8, 0.9), "V_OC sigma prediction beyond tolerance (check ML logic)"

    def test_predict(self):
        """
        Test predictions on the standard organic model
 
        This model is trained on HCEP data.  The prediction mirrors that on the
        organics demo script
        """

        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
        vid = "177" 
  
        resp = client.predict(vid, inputs, method="scalar")
        prediction = resp['candidates'][0]
        self._test_prediction_values(prediction)

    def test_predict_from_distribution(self):
        """
        Test predictions on the standard organic model
 
        Same as `test_predict` but using the `from_distribution` method
        """

        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
        vid = "177" 
  
        resp = client.predict(vid, inputs, method="from_distribution")
        prediction = resp['candidates'][0]
        self._test_prediction_values(prediction)

    def test_predict_custom(self):
        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        input = {"canary_x": "0.5", "temperature": "100", "canary_y": "0.75"}
        resp = client.predict_custom("canary", input)
        prediction = resp['candidates'][0]
        assert 'canary_zz' in prediction.keys()
        assert 'canary_z' in prediction.keys()

    def test_tsne(self):
        """
        Test that we can grab the t-SNE from a pre-trained view
        """
        client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        resp = client.tsne("1623")

        assert len(resp) == 1, "Expected a single tSNE block but got {}".format(len(resp))

        tsne_y = resp[list(resp.keys())[0]]
        assert "x" in tsne_y, "Couldn't find x component of tsne projection"
        assert "y" in tsne_y, "Couldn't find y component of tsne projection"
        assert "z" in tsne_y, "Couldn't find property label for tsne projection"
        assert "uid" in tsne_y, "Couldn't find uid in tsne projection"
        assert "label" in tsne_y, "Couldn't find label in tsne projection"

        assert len(tsne_y["x"]) == len(tsne_y["y"]),     "tSNE components x and y had different lengths"
        assert len(tsne_y["x"]) == len(tsne_y["z"]),     "tSNE components x and z had different lengths"
        assert len(tsne_y["x"]) == len(tsne_y["label"]), "tSNE components x and uid had different lengths"
        assert len(tsne_y["x"]) == len(tsne_y["uid"]),   "tSNE components x and label had different lengths"

