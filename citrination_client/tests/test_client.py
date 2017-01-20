from citrination_client import CitrinationClient
from os import environ
from json import loads
from pypif.obj.system import System
from tempfile import TemporaryDirectory
from pypif.pif import dump
from os.path import join

def test_start_client():
    client = CitrinationClient(environ['CITRINATION_API_KEY'], 'https://stage.citrination.com')


def test_upload_pif():
    client = CitrinationClient(environ['CITRINATION_API_KEY'], 'https://stage.citrination.com')
    dataset = loads(client.create_data_set(name="Tutorial dataset", description="Dataset for tutorial", share=0).content.decode('utf-8'))['id']
    pif = System()
    pif.id = 0

    with TemporaryDirectory() as tmpdir:
        tempname = join(tmpdir, "pif.json")
        with open(tempname, "w") as fp:
            dump(pif, fp)
        response = loads(client.upload_file(tempname, dataset))
    assert response["message"] == "Upload is complete."
