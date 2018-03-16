class Tsne(object):

    def __init__(self):
        self._projections = {}

    def add_projection(self, key, projection):
        self._projections[key] = projection

    def projections(self):
        return self._projections.keys()

    def get_projection(self, key):
        try:
            return self._projections[key]
        except KeyError:
            return None