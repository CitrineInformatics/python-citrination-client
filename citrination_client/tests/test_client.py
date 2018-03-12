from citrination_client import *
from os import environ
import os
from json import loads
from pypif.obj.system import System
from pypif.pif import dump
import random
import string
import time
import pytest

def _almost_equal(test_value, reference_value, tolerance=1.0e-9):
    """
    Numerical equality with a tolerance
    """
    return abs(test_value - reference_value) < tolerance

def assert_run_accepted(view_id, run, client):
    status = client.get_design_run_status(view_id, run.uuid)
    assert status.accepted()

def kill_and_assert_killed(view_id, run, client):
    killed_uid = client.kill_design_run(view_id, run.uuid)

    assert killed_uid == run.uuid

    status = client.get_design_run_status(view_id, run.uuid)
    assert status.killed()

class TestClient():

    @classmethod
    def setup_class(cls):
        cls.client = CitrinationClient(environ['CITRINATION_API_KEY'], environ['CITRINATION_SITE'])
        # Append dataset name with random string because one user can't have more than
        # one dataset with the same name
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        dataset_name = "Tutorial dataset " + random_string
        cls.set_id = loads(cls.client.create_data_set(name=dataset_name, description="Dataset for tutorial", share=0).content.decode('utf-8'))['id']
        cls.test_file_root = './citrination_client/tests/test_files/'

    def _trigger_run(self, client, view_id, num_candidates=10, effort=1, constraints=[], target=Target(name="Property Band gap", objective="Max")):

        return client.submit_design_run(data_view_id=view_id,
                                         num_candidates=num_candidates,
                                         constraints=constraints,
                                         target=target,
                                         effort=effort)

    @pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
    def test_experimental_design(self):
        """
        Tests that a design run can be triggered, the status can be polled, and once it is finished, the results can be retrieved.
        """
        client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
        view_id = "138"
        run = self._trigger_run(client, view_id, constraints=[CategoricalConstraint(name="Property Color",
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
    def test_design_run_effort_limit(self):
        """
        Tests that a design run cannot be submitted with an effort
        value greater than 30
        """
        client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
        view_id = "138"

        try:
            run = self._trigger_run(client, view_id, effort=1000)
            assert False
        except CitrinationClientError:
            assert True

    @pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
    def test_kill_experimental_desing(self):
        """
        Tests that an in progress design run can be killed and the status
        will be reported as killed afterward.
        """
        client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
        view_id = "138"
        run = self._trigger_run(client, view_id)
        assert_run_accepted(view_id, run, client)
        kill_and_assert_killed(view_id, run, client)

    @pytest.mark.skipif(environ['CITRINATION_SITE'] != "https://qa.citrination.com", reason="Design tests only supported on qa")
    def test_can_submit_run_with_no_target(self):
        """
        Tests that a design run can be submitted successfully with no target.
        """
        client = CitrinationClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
        view_id = "138"

        run = self._trigger_run(client, view_id, target=None)

        assert_run_accepted(view_id, run, client)
        kill_and_assert_killed(view_id, run, client)
