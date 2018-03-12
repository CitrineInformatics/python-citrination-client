from citrination_client.base.base_client import BaseClient
import requests

class PredictClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        members = [
            "predict",
            "predict_custom"
        ]
        super(PredictClient, self).__init__(api_key, webserver_host, members)

    def predict(self, model_path, candidates, method="scalar", use_prior=True):
        """
        Predict endpoint

        :param model_name: The model identifier (id number for data views)
        :param candidates: A list of candidates to make predictions on
        :param method:     Method for propagating predictions through model graphs
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """
        body = self._get_predict_body(candidates, method, use_prior)

        url = 'data_views/' + model_path + '/predict'
        response = self._post_json(url, data=body)

        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))

        return response.json()

    def predict_custom(self, model_path, candidates):
        """
        Predict endpoint for a custom model

        :param model_path: The path from the custom model url (https://citrination.com/predict/{{model_path}})
        :param candidates: A list of candidates to make predictions on
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """

        body = self._get_predict_body(candidates)

        endpoint = 'ml_templates/' + model_path + '/predict'
        response = self._post_json(endpoint, data=body)

        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))

        return response.json()

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
