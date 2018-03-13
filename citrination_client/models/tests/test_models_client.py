from citrination_client.client import CitrinationClient
from os import environ

citrination_client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
client = citrination_client.models

def _almost_equal(test_value, reference_value, tolerance=1.0e-9):
    """
    Numerical equality with a tolerance
    """
    return abs(test_value - reference_value) < tolerance

def _assert_prediction_values(prediction):
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


def test_predict():
    """
    Test predictions on the standard organic model

    This model is trained on HCEP data.  The prediction mirrors that on the
    organics demo script
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
    vid = "177" 

    resp = client.predict(vid, inputs, method="scalar")
    prediction = resp['candidates'][0]
    _assert_prediction_values(prediction)

def test_predict_from_distribution():
    """
    Test predictions on the standard organic model

    Same as `test_predict` but using the `from_distribution` method
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
    vid = "177" 

    resp = client.predict(vid, inputs, method="from_distribution")
    prediction = resp['candidates'][0]
    _assert_prediction_values(prediction)

def test_predict_custom():
    input = {"canary_x": "0.5", "temperature": "100", "canary_y": "0.75"}
    resp = client.predict_custom("canary", input)
    prediction = resp['candidates'][0]
    assert 'canary_zz' in prediction.keys()
    assert 'canary_z' in prediction.keys()