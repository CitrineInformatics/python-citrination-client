from citrination_client.client import CitrinationClient
from os import environ
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import random
import string

parent_client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
client = parent_client.model_reports

def test_tsne():
    """
    Test that we can grab the t-SNE from a pre-trained view
    """
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
