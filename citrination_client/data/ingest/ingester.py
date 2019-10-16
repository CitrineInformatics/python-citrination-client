from citrination_client.base import InvalidOptionError, CitrinationClientError
from copy import deepcopy

class ArgumentNotFoundError(CitrinationClientError):
    def __init__(self, message):
        super(message)

class Ingester:
    """
    Class representation of an ingester

    :ivar str ~.display_name:
    :ivar str ~.description:
    :ivar str ~.namespace:
    :ivar str ~.name:
    :ivar str ~.version:
    :ivar str ~.id:
    :ivar ~.arguments: any optional and/or required arguments for the ingester
    :vartype ~.arguments: list of dict
    """

    SEARCH_FIELDS = set([
        'description', 'display_name', 'name', 'namespace', 'version', 'id'
    ])
    """
    Attributes of an Ingester that can be searched when filtering through Ingesters
    via the IngestList#where method.
    """

    def __init__(self, ingester):
        """
        Constructor.

        :param ingester: An ingester
        :type ingester: dict
        """
        self._ingester = ingester;
        self.display_name = ingester['display_name']
        self.description = ingester['description']
        self.namespace = ingester['namespace']
        self.name = ingester['name']
        self.version = ingester['version']
        self.id = ingester['id']
        self.arguments = deepcopy(ingester['arguments']) or []

    @classmethod
    def validate_search_key(klass, key, suppress_error = True):
        """
        Returns whether or not a key correlates to a field that can be searched

        :param key: The key to check
        :type key: str
        :param suppress_error: When false, will raise an error for invalid keys
        :type suppress_error: bool
        :return: True if the key is valid, otherwise false
        :rtype: bool
        """
        key_present = key in klass.SEARCH_FIELDS

        if key_present or suppress_error:
            return key_present
        elif not key_present:
            raise InvalidOptionError(
                'Invalid key {}, accepted keys are {}'.format(
                    key, klass.SEARCH_FIELDS
                )
            )

    def clone(self):
        """
        Returns a copy of the ingester. Used by the IngestClient to apply values
        to a copy of the selected ingester before submission.

        :return: Returns a copy of the ingester based on a deep clone of the
                 _ingester dict that instantiated the instance.
        :return: class:`Ingester`
        """
        return self.__class__(deepcopy(self._ingester))

    def find_argument(self, name):
        """
        Finds an argument in self.arguments that matches the provided name.
        If there are no matches, raises an ArgumentNotFoundError

        :param name: The name of the argument
        :type name: str
        :return: The argument whose name matched
        :rtype: dict
        """
        try:
            # Find the first argument whose name matches
            return next(
                filter(lambda argument: argument['name'] == name, self.arguments)
            )
        except StopIteration:
            raise ArgumentNotFoundError(
                'Unable to find argument with name {}'.format(name)
            )

    def as_json(self):
        """
        Returns a dict that can used for ingest submission

        :return: A dict representation of the ingester
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "namespace": self.namespace,
            "version": self.version,
            "display_name": self.display_name,
            "description": self.description,
            "arguments": self.arguments
        }

    def __str__(self):
        return "<Ingester id='{}' display_name='{}' description='{}' num_arguments={}>".format(
            self.id, self.display_name, self.description, len(self.arguments)
        )
