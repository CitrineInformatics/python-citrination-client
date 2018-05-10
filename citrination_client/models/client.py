from citrination_client.base.base_client import BaseClient
from citrination_client.models import *
from citrination_client.models.design import *
from citrination_client.models import routes as routes
from citrination_client.base.errors import CitrinationClientError
from citrination_client.data import Dataset
from citrination_client.models.data_view import DataView
from citrination_client.models.columns.column_factory import ColumnFactory

import time

class ModelsClient(BaseClient):
    """
    A client that encapsulates interactions with models on Citrination.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False):
        members = [
            "tsne",
            "predict"
        ]
        super(ModelsClient, self).__init__(api_key, webserver_host, members, suppress_warnings=suppress_warnings)

    def tsne(self, data_view_id):
        """
        Get the t-SNE projection, including responses and tags.

        :param data_view_id: The ID of the data view to retrieve TSNE from
        :type data_view_id: int
        :return: The TSNE analysis
        :rtype: :class:`Tsne`
        """
        analysis = self._data_analysis(data_view_id)
        projections = analysis['projections']
        tsne = Tsne()
        for k, v in projections.items():
            projection = Projection(
                xs=v['x'],
                ys=v['y'],
                responses=v['label'],
                tags=v['inputs'],
                uids=v['uid']
            )
            tsne.add_projection(k, projection)

        return tsne

    def predict(self, data_view_id, candidates, method="scalar", use_prior=True):
        """
        Predict endpoint

        :param data_view_id: The ID of the data view to use for prediction
        :type data_view_id: str
        :param candidates: A list of candidates to make predictions on
        :type candidates: list of dicts
        :param method: Method for propagating predictions through model
            graphs
        :type method: str ("scalar" or "from_distribution")
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :type use_prior: bool
        :return: The results of the prediction
        :rtype: list of :class:`PredictionResult`
        """
        body = self._get_predict_body(candidates, method, use_prior)
        failure_message = "Error while making prediction for data view {}".format(data_view_id)
        response_dict = self._get_success_json(
            self._post_json(routes.data_view_predict(data_view_id), data=body, failure_message=failure_message))
        candidate_dicts = response_dict["candidates"]
        return list(
            map(
                lambda c: _get_prediction_result_from_candidate(c), candidate_dicts
            )
        )

    def _data_analysis(self, data_view_id):
        """
        Data analysis endpoint.

        :param data_view_id: The model identifier (id number for data views)
        :type data_view_id: str
        :return: dictionary containing information about the data, e.g. dCorr and tsne
        """
        failure_message = "Error while retrieving data analysis for data view {}".format(data_view_id)
        return self._get_success_json(self._get(routes.data_analysis(data_view_id), failure_message=failure_message))

    def _get_predict_body(self, candidates, method="scalar", use_prior=True):
        if not (method == "scalar" or method == "from_distribution"):
            raise ValueError("{} method not supported".format(method))

        # If a single candidate is passed, wrap in a list for the user
        if not isinstance(candidates, list):
            candidates = [candidates]

        return {
            "predictionRequest": {
                "predictionSource": method,
                "usePrior":         use_prior,
                "candidates":       candidates
            }
        }

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
            "target":         target,
            "effort":         effort,
            "constraints":    constraint_dicts,
            "sampler":        sampler
        }

        url = routes.submit_data_view_design(data_view_id)

        response = self._post_json(url, body).json()

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

        url = routes.get_data_view_design_status(data_view_id, run_uuid)

        response = self._get(url).json()

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

        url = routes.get_data_view_design_results(data_view_id, run_uuid)

        response = self._get(url).json()

        result = response["data"]

        return DesignResults(
            best_materials=result.get("best_material_results"),
            next_experiments=result.get("next_experiment_results")
        )

    def get_data_view(self, data_view_id):
        """
        Retrieves a summary of information for a given data view
            - view id
            - name
            - description
            - columns

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        """

        url = routes.get_data_view(data_view_id)

        response = self._get(url).json()

        result = response["data"]["data_view"]

        datasets_list = []
        for dataset in result["datasets"]:
            datasets_list.append(Dataset(
                name=dataset["name"],
                id=dataset["id"],
                description=dataset["description"]
            ))

        columns_list = []
        for column in result["columns"]:
            columns_list.append(ColumnFactory.from_dict(column))

        return DataView(
            view_id=data_view_id,
            name=result["name"],
            description=result["description"],
            datasets=datasets_list,
            columns=columns_list,
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

        url = routes.kill_data_view_design_run(data_view_id, run_uuid)

        response = self._delete(url).json()
        return response["data"]["uid"]

    def get_data_view_service_status(self, data_view_id):
        """
        Retrieves the status for all of the services associated with a data view:
            - predict
            - experimental_design
            - data_reports
            - model_reports

        :param data_view_id: The ID number of the data view to which the
            run belongs, as a string
        :type data_view_id: str
        :return: A :class:`DataViewStatus`
        :rtype: DataViewStatus
        """

        url = routes.get_data_view_status(data_view_id)

        response = self._get(url).json()

        result = response["data"]["status"]

        return DataViewStatus(
            predict = ServiceStatus.from_response_dict(result["predict"]),
            experimental_design = ServiceStatus.from_response_dict(result["experimental_design"]),
            data_reports = ServiceStatus.from_response_dict(result["data_reports"]),
            model_reports = ServiceStatus.from_response_dict(result["model_reports"])
        )

def _get_prediction_result_from_candidate(candidate_dict):
    result = PredictionResult()
    for k, v in candidate_dict.items():
        result.add_value(k, PredictedValue(k, v[0], v[1]))

    return result
