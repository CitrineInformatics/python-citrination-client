class PredictionResult(object):
    """
    The collection of predicted values resulting from a prediction.
    """

    def __init__(self):
        self._values = {}

    def add_value(self, key, value):
        """
        Registers a predicted value in the result.

        :param key: The descriptor key for the predicted value
        :type key: str
        :param value: A :class:`PredictedValue`
        :type value: object
        :return: None
        :rtype: NoneType
        """
        self._values[key] = value

    def get_value(self, key):
        """
        Retrieves a predicted value.

        :param key: A descriptor key for a registered predicted value.
        :type key: str
        :return: The value stored at the provided descriptor key. None if no key is provided.
        :rtype: :class:`PredictedValue`
        """
        try:
            return self._values[key]
        except KeyError:
            return None

    def all_keys(self):
        """
        Retrieves a list of all the values which were predicted.

        :return: A list of keys for which predictions have been made and can
            be retrieved using `get_value`
        :rtype: list of str
        """

        return self._values.keys()