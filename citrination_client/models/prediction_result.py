class PredictionResult(object):
    """
    The collection of predicted values resulting from a prediction.
    """

    def __init__(self):
        self._values = {}

    def add_value(self, key, value):
        """
        Registers a predicted value in the result.

        :param key: The descriptor key for the predicted value
        :param value: A :class:`PredictedValue`
        :return: None
        """
        self._values[key] = value

    def get_value(self, key):
        """
        Retrieves a predicted value.

        :param key: A descriptor key for a registered predicted value.
        :return: a :class:`PredictedValue`
        """
        try:
            return self._values[key]
        except KeyError:
            return None