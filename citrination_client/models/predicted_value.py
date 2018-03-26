class PredictedValue(object):
    """
    The value/loss output from a prediction.
    """

    def __init__(self, key, value, loss=None):
        """
        Constructor.

        :param key: The descriptor key for the prediction
        :type key: str
        :param value: The predicted value
        :type value: str or float
        :param loss: The loss for the prediction
        :type loss: float
        """
        self._key = key
        self._value = value
        self._loss = loss

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @key.deleter
    def key(self):
        self._key = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self):
        self._value = None

    @property
    def loss(self):
        return self._loss

    @loss.setter
    def loss(self, value):
        self._loss = value

    @loss.deleter
    def loss(self):
        self._loss = None