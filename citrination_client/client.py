from citrination_client.model_reports import ModelReportsClient
from citrination_client.predict.client import PredictClient
from citrination_client.search.client import SearchClient
from citrination_client.data_management.client import DataManagementClient

class CitrinationClient(object):

  def __init__(self, api_key, host="https://citrination.com"):
    self.model_reports = ModelReportsClient(api_key, host)
    self.predict = PredictClient(api_key, host)
    self.search = SearchClient(api_key, host)
    self.data_management = DataManagementClient(api_key, host)

  def __repr__(self):
    return "['model_reports', 'predict', 'search', 'data_management']"