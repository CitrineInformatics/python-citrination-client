from citrination_client.base.base_client import BaseClient

class ModelReportsClient(BaseClient):

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

    def _data_analysis(self, model_name):
        """
        Data analysis endpoint
        :param model_name: The model identifier (id number for data views)
        :return: dictionary containing information about the data, e.g. dCorr and tsne
        """
        return self._get('data_views/' + model_name + '/data_analysis').json()
