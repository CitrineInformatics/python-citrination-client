from citrination_client.models import PredictionResult
from citrination_client.models import PredictedValue

def test_can_list_all_stored_predicted_values():
    """
    Tests that for a prediction result which stores many
    predicted values, all_keys correctly lists the keys under
    which each of those values is registered
    """

    k1 = "Property Band Gap"
    v1 = 1.0
    pv1 = PredictedValue(k1, v1)

    k2 = "Property Color"
    v2 = 1.0
    pv2 = PredictedValue(k2, v2)

    k3 = "Property Transmission"
    v3 = 1.0
    pv3 = PredictedValue(k3, v3)

    pr = PredictionResult()

    pr.add_value(k1, pv1)
    pr.add_value(k2, pv2)
    pr.add_value(k3, pv3)

    assert k1 in pr.all_keys()
    assert k2 in pr.all_keys()
    assert k3 in pr.all_keys()