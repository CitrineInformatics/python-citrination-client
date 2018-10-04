from citrination_client.client import CitrinationClient
from citrination_client.models import *
from citrination_client.models.columns import *
from os import environ
import pytest

import time
from citrination_client.base.errors import *

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

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Predict tests only supported on open citrination")
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

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Retrain tests only supported on open citrination")
def test_retrain():
    """
    Test that we can trigger a retrain
    """
    resp = client.retrain("27")
    assert resp == True

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Predict tests only supported on open citrination")
def test_predict():
    """
    Test predictions on the standard organic model

    This model is trained on HCEP data.  The prediction mirrors that on the
    organics demo script
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}]
    vid = 177

    prediction_result = client.predict(vid, inputs, method="scalar")[0]
    _assert_prediction_values(prediction_result)

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Predict tests only supported on open citrination")
def test_template_latest_version():
    """
    Tests that the latest version of the template can be returned
    """
    vid = 177
    latest_template = client.template_latest_version('view_ml_{}_1'.format(vid))
    assert isinstance(latest_template, int)

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Predict tests only supported on open citrination")
def test_multiple_predict_candidates():
    """
    Tests that if you pass multiple candidates for prediction into the
    prediction method, you will receive multiple prediction results.
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"},{"SMILES": "C=C"}]
    vid = 177

    prediction_results = client.predict(vid, inputs, method="scalar")
    assert len(prediction_results) == 2
    assert type(prediction_results[0]) == PredictionResult
    assert type(prediction_results[1]) == PredictionResult

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Predict tests only supported on open citrination")
def test_predict_from_distribution():
    """
    Test predictions on the standard organic model

    Same as `test_predict` but using the `from_distribution` method
    """

    inputs = [{"SMILES": "c1(C=O)cc(OC)c(O)cc1"}, ]
    vid = "177"

    prediction_result = client.predict(vid, inputs, method="from_distribution")[0]
    _assert_prediction_values(prediction_result)


def assert_run_accepted(view_id, run, client):
    status = client.get_design_run_status(view_id, run.uuid)
    assert status.accepted()

def kill_and_assert_killed(view_id, run, client):
    killed_uid = client.kill_design_run(view_id, run.uuid)

    assert killed_uid == run.uuid

    status = client.get_design_run_status(view_id, run.uuid)
    assert status.killed()

def _trigger_run(client, view_id, num_candidates=10, effort=1, constraints=[], target=Target(name="Property Band gap", objective="Max")):

    return client.submit_design_run(data_view_id=view_id,
                                     num_candidates=num_candidates,
                                     constraints=constraints,
                                     target=target,
                                     effort=effort)

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
def test_experimental_design():
    """
    Tests that a design run can be triggered, the status can be polled, and once it is finished, the results can be retrieved.
    """
    view_id = "138"
    run = _trigger_run(client, view_id, constraints=[CategoricalConstraint(name="Property Color",
                                             accepted_categories=["Gray"])])

    try:
        status = client.get_design_run_status(view_id, run.uuid)
        while not status.finished():
            time.sleep(1)
            status = client.get_design_run_status(view_id, run.uuid)
    except Exception:
        client.kill_design_run(view_id, run.uuid)
        raise

    results = client.get_design_run_results(view_id, run.uuid)
    assert len(results.next_experiments) > 0
    assert len(results.best_materials) > 0

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
def test_experimental_design_infinity_constraint():
    """
    Tests that a design run can be triggered with an Infinity Constraint
    """
    view_id = "138"
    run = _trigger_run(client, view_id, target=None, constraints=[RealRangeConstraint(name="Property Band gap", minimum=0, maximum=float("inf"))])

    assert_run_accepted(view_id, run, client)
    kill_and_assert_killed(view_id, run, client)


@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
def test_design_run_effort_limit():
    """
    Tests that a design run cannot be submitted with an effort
    value greater than 30
    """
    view_id = "138"

    try:
        run = _trigger_run(client, view_id, effort=1000)
        assert False
    except CitrinationClientError:
        assert True

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
def test_kill_experimental_desing():
    """
    Tests that an in progress design run can be killed and the status
    will be reported as killed afterward.
    """
    view_id = "138"
    run = _trigger_run(client, view_id)
    assert_run_accepted(view_id, run, client)
    kill_and_assert_killed(view_id, run, client)

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
def test_can_submit_run_with_no_target():
    """
    Tests that a design run can be submitted successfully with no target.
    """
    view_id = "138"

    run = _trigger_run(client, view_id, target=None)

    assert_run_accepted(view_id, run, client)
    kill_and_assert_killed(view_id, run, client)

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Data view status tests only supported on open")
def test_data_view_status_reports_services_ready():
    """
    Tests that a data view on open citrination which has successfully trained reports
    the status of it's services as ready.
    """
    view_id = "524"

    status = client.get_data_view_service_status(data_view_id=view_id)

    # There is no way to guarantee that this view is not retraining, but the
    # majority of the time it should be in a stable, trained state
    assert status.predict.is_ready()
    assert status.experimental_design.is_ready()
    assert status.data_reports.is_ready()
    assert status.model_reports.is_ready()

@pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://citrination.com", reason="Data view summary tests currently only supported on public")
def test_get_data_view():
    """
    Tests that get_data_view returns the summary information for a given data view
    """
    view_id = "524"

    data_view = client.get_data_view(data_view_id=view_id)

    assert data_view.name == "Band Gap Demo"
    assert len(data_view.columns) == 4
    assert data_view.columns[0].name == "Crystallinity"
    assert len(data_view.datasets) == 1
    assert data_view.datasets[0].name == "Band gaps from Strehlow and Cook"
