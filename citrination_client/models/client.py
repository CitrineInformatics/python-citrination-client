from citrination_client.base.base_client import BaseClient
from citrination_client.models import *

from citrination_client.models import routes as routes

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
        :type data_view_id: int
        :param candidates: A list of candidates to make predictions on
        :type candidates: list of dicts
        :param method: Method for propagating predictions through model
            graphs
        :type method: str ("scalar" or "from_distribution")
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :type use_prior: bool
        :return: The result of the prediction
        :rtype: :class:`PredictionResult`
        """
        body = self._get_predict_body(candidates, method, use_prior)
        failure_message = "Error while making prediction for data view {}".format(data_view_id)
        response_dict = self._get_success_json(self._post_json(routes.data_view_predict(data_view_id), data=body, failure_message=failure_message))
        return _get_prediction_result_from_response(response_dict)

    def _data_analysis(self, data_view_id):
        """
        Data analysis endpoint.

        :param data_view_id: The model identifier (id number for data views)
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
                "usePrior": use_prior,
                "candidates": candidates
                }
            }

def _get_prediction_result_from_response(response):
    candidate = response['candidates'][0]
    result = PredictionResult()
    for k,v in candidate.items():
        result.add_value(k, PredictedValue(k, v[0], v[1]))

    return result
