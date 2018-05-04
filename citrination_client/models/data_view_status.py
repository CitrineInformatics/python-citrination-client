class DataViewStatus(object):
    """
    A summary of each of the services a data view exposes.
    """

    def __init__(predict=None, design=None, data_analysis=None, model_reports=None):
        """
        Constructor.

        :param predict: The status predict
        :type predict: ServiceStatus
        :param design: The status of design
        :type design: ServiceStatus
        :param data_analysis: The status of data_analysis
        :type data_analysis: ServiceStatus
        :param model_reports: The status of model reports
        :type model_reports: ServiceStatus
        """
        self._predict       = predict
        self._design        = design
        self._data_analysis = data_analysis
        self._model_reports = model_reports

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
    def design(self):
        return self._design

    @design.setter
    def design(self, value):
        self._design = value

    @design.deleter
    def design(self):
        self._design = None

    @property
    def data_an(self):
        return self._data_analysis

    @data_an.setter
    def data_an(self, value):
        self._data_analysis = value

    @data_an.deleter
    def data_an(self):
        self._data_analysis = None

    @property
    def model_reports(self):
        return self._model_reports

    @model_reports.setter
    def model_reports(self, value):
        self._model_reports = value

    @model_reports.deleter
    def model_reports(self):
        self._model_reports = None
