from pypif.util.case import to_camel_case
from pypif.util.case import keys_to_snake_case

import json

class QueryEncoder(json.JSONEncoder):
    """
    Class used to convert a query to json.
    """

    def default(self, obj):
        """
        Convert an object to a form ready to dump to json.

        :param obj: Object being serialized. The type of this object must be one of the following: None; a single object derived from the Pio class; or a list of objects, each derived from the Pio class.
        :return: List of dictionaries, each representing a physical information object, ready to be serialized.
        """
        if obj is None:
            return []
        elif isinstance(obj, list):
            return [i.as_dictionary() for i in obj]
        elif isinstance(obj, dict):
            return self._keys_to_camel_case(obj)
        else:
            return obj.as_dictionary()

    def _keys_to_camel_case(self, obj):
        """
        Make a copy of a dictionary with all keys converted to camel case. This is just calls to_camel_case on each of the keys in the dictionary and returns a new dictionary.

        :param obj: Dictionary to convert keys to camel case.
        :return: Dictionary with the input values and all keys in camel case
        """
        return dict((to_camel_case(key), value) for (key, value) in obj.items())
