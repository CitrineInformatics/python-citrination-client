from copy import deepcopy

class ModelReport(object):
    """
    An abstraction of a model report that wraps access to various sections
    of the report.
    """

    """
    :param raw_report: the dict representation of model report JSON
    :type: dict
    """
    def __init__(self, raw_report):
        self._raw_report = raw_report

    @property
    def model_name(self):
        """
        :rtype: str
        """
        return self._raw_report['model_name']

    @property
    def performance(self):
        """
        :rtype: dict
        """
        return self._raw_report['error_metrics']

    @property
    def feature_importances(self):
        """
        :rtype: list of dict
        """
        return self._raw_report['feature_importances']

    @property
    def model_settings(self):
        """
        :rtype: dict
        """
        return self._raw_report['model_settings']

    """
    WARNING - the dict format returned is unstable and may change over time.

    :return: a copy of the raw report that backs the instance.
    :rtype: dict
    """
    def as_json(self):
        return deepcopy(self._raw_report)
