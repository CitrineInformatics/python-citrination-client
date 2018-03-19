class Projection(object):
    """
    A projection to be included in the TSNE analysis.
    """

    def __init__(self, xs, ys, zs, labels, uids):
        """
        Constructor.

        :param xs: A list of x values of the projection.
        :param ys: A list of y values of the projection.
        :param zs: A list of z values of the projection.
        :param labels: A list of labels for the projected points
        :param uids: A list of record UIDs for the projected points
        """
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