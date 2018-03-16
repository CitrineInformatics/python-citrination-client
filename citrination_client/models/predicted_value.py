class PredictedValue(object):

    def __init__(self, key, value, sigma=None):
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