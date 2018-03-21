from citrination_client.models import ModelsClient
from citrination_client.search import SearchClient
from citrination_client.data import DataClient
from citrination_client.errors import *
from citrination_client.design import *
from citrination_client.util.credentials import get_preferred_credentials

"""
Generates a lambda method in a closure such that the
client and method_name are constant (avoides reassignment
in the assignment loop in the client class)
"""
def _generate_lambda_proxy_method(client, method_name):
    subclient_m = getattr(client, method_name)
    return lambda *args, **kw: subclient_m(*args, **kw)

class CitrinationClient(object):

    def __init__(self, api_key=None, site=None):
        api_key, site = get_preferred_credentials(api_key, site)
        self.models = ModelsClient(api_key, site)
        self.search = SearchClient(api_key, site)
        self.data = DataClient(api_key, site)

        clients = [self.models, self.search, self.data]

        for client in clients:
            client_methods = [a for a in dir(client) if not a.startswith('_')]
            for method in client_methods:
                setattr(self, method, _generate_lambda_proxy_method(client, method))


    def __repr__(self):
        return "['models', 'search', 'data']"

    def submit_design_run(self, data_view_id, num_candidates, effort, target=None, constraints=[], sampler="Default"):
        """
        Submits a new experimental design run

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param num_candidates: The number of candidates to return
        :type num_candidates: int
        :param target: An :class:``Target`` instance representing
            the design run optimization target
        :type target: :class:``Target``
        :param constraints: An array of design constraints (instances of
            objects which extend :class:``BaseConstraint``)
        :type constraints: list of :class:``BaseConstraint``
        :param sampler: The name of the sampler to use during the design run:
            either "Default" or "This view"
        :type sampler: str
        :return: A :class:`DesignRun` instance containing the UID of the
            new run
        """

        if effort > 30:
            raise CitrinationClientError("Parameter effort must be less than 30 to trigger a design run")

        if target is not None:
            target = target.to_dict()

        constraint_dicts = [c.to_dict() for c in constraints]

        body = {
            "num_candidates": num_candidates,
            "target": target,
            "effort": effort,
            "constraints": constraint_dicts,
            "sampler": sampler
        }

        url = "{}/data_views/{}/experimental_design".format(self.api_url,
                                                            data_view_id)

        response = self._post_with_version_check(url, data=json.dumps(body), headers=self.headers).json()

        return DesignRun(response["data"]["design_run"]["uid"])

    def get_design_run_status(self, data_view_id, run_uuid):
        """
        Retrieves the status of an in progress or completed design run

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param run_uuid: The UUID of the design run to retrieve status for
        :type run_uuid: str
        :return: A :class:`ProcessStatus` object
        """

        url = "{}/data_views/{}/experimental_design/{}/status".format(self.api_url, data_view_id, run_uuid)

        response = self._get_with_version_check(url, headers=self.headers).json()

        status = response["data"]

        return ProcessStatus(
            result=status.get("result"),
            progress=status.get("progress"),
            status=status.get("status"),
            messages=status.get("messages")
        )

    def get_design_run_results(self, data_view_id, run_uuid):
        """
        Retrieves the results of an existing designrun

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param run_uuid: The UUID of the design run to retrieve results from
        :type run_uuid: str
        :return: A :class:`DesignResults` object
        """

        url = "{}/data_views/{}/experimental_design/{}/results".format(self.api_url, data_view_id, run_uuid)

        response = self._get_with_version_check(url, headers=self.headers).json()

        result = response["data"]

        return DesignResults(
            best_materials=result.get("best_material_results"),
            next_experiments=result.get("next_experiment_results")
        )

    def kill_design_run(self, data_view_id, run_uuid):
        """
        Kills an in progress experimental design run

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :param run_uuid: The UUID of the design run to kill
        :type run_uuid: str
        :return: The UUID of the design run
        """

        url = "{}/data_views/{}/experimental_design/{}".format(self.api_url, data_view_id, run_uuid)

        response = self._delete_with_version_check(url, headers=self.headers).json()

        return response["data"]["uid"]