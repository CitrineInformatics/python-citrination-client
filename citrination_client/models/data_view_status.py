class DataViewStatus(object):
    """
    A summary of each of the services a data view exposes.
    """

    def __init__(self, predict=None, experimental_design=None, data_reports=None, model_reports=None):
        """
        Constructor.

        :param predict: The status predict
        :type predict: ServiceStatus
        :param experimental_design: The status of experimental_design
        :type experimental_design: ServiceStatus
        :param data_reports: The status of data_analysis
        :type data_reports: ServiceStatus
        :param model_reports: The status of model reports
        :type model_reports: ServiceStatus
        """
        self._predict             = predict
        self._experimental_design = experimental_design
        self._data_reports        = data_reports
        self._model_reports       = model_reports

    @property
    def predict(self):
        return self._predict

    @predict.setter
    def predict(self, value):
        self._predict = value

    @predict.deleter
    def predict(self):
        self._predict = None

    @property
    def experimental_design(self):
        return self._experimental_design

    @experimental_design.setter
    def experimental_design(self, value):
        self._experimental_design = value

    @experimental_design.deleter
    def experimental_design(self):
        self._experimental_design = None

    @property
    def data_reports(self):
        return self._data_reports

    @data_reports.setter
    def data_reports(self, value):
        self._data_reports = value

    @data_reports.deleter
    def data_reports(self):
        self._data_reports = None

    @property
    def model_reports(self):
        return self._model_reports

    @model_reports.setter
    def model_reports(self, value):
        self._model_reports = value

    @model_reports.deleter
    def model_reports(self):
        self._model_reports = None
