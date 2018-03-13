from citrination_client.base.base_client import BaseClient
from citrination_client.util import http as http_util
import routes

class ModelsClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        members = [
            "tsne",
            "predict",
            "predict_custom"            
        ]
        super(ModelsClient, self).__init__(api_key, webserver_host, members)

    def tsne(self, model_name):
        """
        Get the t-SNE projection, including z-values and labels
        :param model_name: The model identifier (id number for data views)
        :return: dictionary containing property names and the projection for each
        """
        analysis = self._data_analysis(model_name)
        projections = analysis['projections']
        cleaned = {}
        for k, v in projections.items():
            d = {}
            d['x'] = v['x']
            d['y'] = v['y']
            d['z'] = v['label']
            d['label'] = v['inputs']
            d['uid'] = v['uid']
            cleaned[k] = d

        return cleaned

    def predict(self, data_view_id, candidates, method="scalar", use_prior=True):
        """
        Predict endpoint

        :param data_view_id: The model identifier (id number for data views)
        :param candidates: A list of candidates to make predictions on
        :param method:     Method for propagating predictions through model graphs
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """
        body = self._get_predict_body(candidates, method, use_prior)

        return http_util.get_success_json(
            self._post_json(routes.data_view_predict(data_view_id), data=body),
            "Error while making prediction for data view {}".format(data_view_id)
        )

    def predict_custom(self, model_path, candidates):
        """
        Predict endpoint for a custom model

        :param model_path: The path from the custom model url (https://citrination.com/predict/{{model_path}})
        :param candidates: A list of candidates to make predictions on
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """

        body = self._get_predict_body(candidates)

        return http_util.get_success_json(
            self._post_json(routes.custom_model_predict(model_path), data=body),
            "Error while making prediction for custom model {}".format(model_path)
        )

    def _data_analysis(self, data_view_id):
        """
        Data analysis endpoint
        :param data_view_id: The model identifier (id number for data views)
        :return: dictionary containing information about the data, e.g. dCorr and tsne
        """
        return http_util.get_success_json(
            self._get(routes.data_analysis(data_view_id)),
            "Error while retrieving data analysis for data view {}".format(data_view_id)
        )

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