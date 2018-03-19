class PredictedValue(object):
    """
    The value/sigma output from a prediction.
    """

    def __init__(self, key, value, sigma=None):
        """
        Constructor.

        :param key: The descriptor key for the prediction
        :param value: The predicted value
        :param sigma: If the predicted value is a real number, the sigma
            for the prediction
        """
        self._key = key
        self._value = value
        if type(value) == str:
            self._sigma = None
        else:
            self._sigma = sigma

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def sigma(self):
        return self._sigma