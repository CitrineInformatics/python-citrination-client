class Tsne(object):
    """
    A TSNE analysis which can be extracted from the data analysis
    for a trained model on Citrination.
    """

    def __init__(self):
        """
        Constructor
        """
        self._projections = {}

    def add_projection(self, key, projection):
        """
        Register a projection under a descriptor key.

        :param key: The descriptor key for the projection
        :type key: str
        :param projection: The projection for the provided descriptor key
        :type projection: :class:`Projection`
        """
        self._projections[key] = projection

    def projections(self):
        """
        List the descriptor keys with registered projections.

        :return: List of descriptor keys
        """
        return self._projections.keys()

    def get_projection(self, key):
        """
        Retrieves the projection registered under a particular
        descriptor key.

        :param key: A descriptor key
        :return: A :class:`Projection`
        """
        return self._projections.get(key)