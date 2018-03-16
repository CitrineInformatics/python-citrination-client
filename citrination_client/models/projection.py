class Projection(object):

    def __init__(self, xs, ys, zs, labels, uids):
        self._xs = xs
        self._ys = ys
        self._zs = zs
        self._labels = labels
        self._uids = uids

    @property
    def xs(self):
        return self._xs

    @property
    def ys(self):
        return self._ys

    @property
    def zs(self):
        return self._zs

    @property
    def labels(self):
        return self._labels

    @property
    def uids(self):
        return self._uids