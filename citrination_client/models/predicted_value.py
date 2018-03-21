class PredictedValue(object):
    """
    The value/loss output from a prediction.
    """

    def __init__(self, key, value, loss=None):
        """
        Constructor.

        :param key: The descriptor key for the prediction
        :param value: The predicted value
        :param loss: If the predicted value is a real number, the loss
            for the prediction
        """
        self._key = key
        self._value = value
        self._loss = loss

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def loss(self):
        return self._loss