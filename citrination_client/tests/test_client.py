from citrination_client import CitrinationClient
from os import environ
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import pytest


def test_start_client():
    client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])


def test_upload_pif():
    client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
    dataset = loads(client.create_data_set(name="Tutorial dataset", description="Dataset for tutorial", share=0).content.decode('utf-8'))['id']
    pif = System()
    pif.id = 0

    with open("tmp.json", "w") as fp:
        dump(pif, fp)
    response = loads(client.upload_file("tmp.json", dataset))
    assert response["message"] == "Upload is complete."


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

test_predict_custom()
