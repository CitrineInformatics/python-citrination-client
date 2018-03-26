class Projection(object):
    """
    A projection to be included in the TSNE analysis.
    """

    def __init__(self, xs, ys, responses, tags, uids):
        """
        Constructor.

        :param xs: A list of x values of the projection.
        :type xs: list of floats
        :param ys: A list of y values of the projection.
        :type ys: list of floats
        :param responses: A list of z values of the projection.
        :type responses: list of floats
        :param tags: A list of tags for the projected points
        :type tags: list of strings
        :param uids: A list of record UIDs for the projected points
        :type uids: list of strings
        """
        self._xs = xs
        self._ys = ys
        self._responses = responses
        self._tags = tags
        self._uids = uids

    @property
    def xs(self):
        return self._xs

    @property
    def ys(self):
        return self._ys

    @property
    def responses(self):
        return self._responses

    @property
    def tags(self):
        return self._tags

    @property
    def uids(self):
        return self._uids