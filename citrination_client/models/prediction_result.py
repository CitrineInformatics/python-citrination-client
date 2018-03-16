class PredictionResult(object):

    def __init__(self):
        self._values = {}

    def add_value(self, key, value):
        self._values[key] = value

    def get_value(self, key):
        try:
            return self._values[key]
        except KeyError:
            return None