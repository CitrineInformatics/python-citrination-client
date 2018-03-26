from citrination_client.client import CitrinationClient
from os import environ

citrination_client = CitrinationClient(environ["CITRINATION_API_KEY"])
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
    assert prediction.get_value('Mass')  is not None, "Mass prediction missing (check ML logic)"
    assert prediction.get_value(egap)    is not None, "E_gap prediction missing (check ML logic)"
    assert prediction.get_value(voltage) is not None, "V_OC prediction missing (check ML logic)"

    assert _almost_equal(prediction.get_value('Mass').value, 250,  60.0), "Mass mean prediction beyond tolerance (check ML logic)"
    assert _almost_equal(prediction.get_value('Mass').loss, 30.0, 40.0), "Mass loss prediction beyond tolerance (check ML logic)"
    assert _almost_equal(prediction.get_value(egap).value, 2.6,  0.7), "E_gap mean prediction beyond tolerance (check ML logic)"
    assert _almost_equal(prediction.get_value(egap).loss, 0.50, 0.55), "E_gap loss prediction beyond tolerance (check ML logic)"
    assert _almost_equal(prediction.get_value(voltage).value, 1.0, 0.9), "V_OC mean prediction beyond tolerance (check ML logic)"
    assert _almost_equal(prediction.get_value(voltage).loss, 0.8, 0.9), "V_OC loss prediction beyond tolerance (check ML logic)"

def test_tsne():
    """
    Test that we can grab the t-SNE from a pre-trained view
    """
    resp = client.tsne("1623")


    tsne_y = resp.get_projection('Property  y')
    assert tsne_y.xs is not None, "Couldn't find x component of tsne projection"
    assert tsne_y.ys is not None, "Couldn't find y component of tsne projection"
    assert tsne_y.responses is not None, "Couldn't find property label for tsne projection"
    assert tsne_y.uids is not None, "Couldn't find uid in tsne projection"
    assert tsne_y.tags is not None, "Couldn't find label in tsne projection"

    assert len(tsne_y.xs) == len(tsne_y.ys),     "tSNE components x and y had different lengths"
    assert len(tsne_y.xs) == len(tsne_y.responses),     "tSNE components x and z had different lengths"
    assert len(tsne_y.xs) == len(tsne_y.tags), "tSNE components x and uid had different lengths"
    assert len(tsne_y.xs) == len(tsne_y.uids),   "tSNE components x and label had different lengths"


def test_predict():
    """
    Test predictions on the standard organic model

    This model is trained on HCEP data.  The prediction mirrors that on the
    organics demo script
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}]
    vid = 177

    prediction_result = client.predict(vid, inputs, method="scalar")
    _assert_prediction_values(prediction_result)

def test_predict_from_distribution():
    """
    Test predictions on the standard organic model

    Same as `test_predict` but using the `from_distribution` method
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
    vid = "177" 

    prediction_result = client.predict(vid, inputs, method="from_distribution")
    _assert_prediction_values(prediction_result)