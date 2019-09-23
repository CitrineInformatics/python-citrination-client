from citrination_client.data.ingest import Ingester
from citrination_client.base import CitrinationClientError
import pdb

class IngesterNotFoundError(CitrinationClientError):
    def __init__(self, message):
        super(message)

class IngesterList:
    """
    Class representation of a list of ingesters available for data upload on
    Citrination.
    """

    def __init__(self, ingesters):
        """
        Constructor.

        :param ingesters: A list of ingesters
        :type ingesters: Union[list, :class:`IngesterList`]
        """
        if not isinstance(ingesters, list):
            raise TypeError('Expected ingesters to be of type list')
        else:
            self.ingesters = list(
                map(
                    lambda ingester: self._coerce_ingester(ingester), ingesters
                )
            )

    @property
    def ingester_count(self):
        """
        Returns the count of how many Ingesters are in the list

        :return: number of Ingesters in self.ingesters
        :rtype: int
        """
        return len(self.ingesters)

    def find_by_id(self, id):
        """
        Finds the ingester whose id matches the provided id

        :param id: The id of the desired ingester
        :type id: str

        :return: An ingester
        :rtype: :class:`Ingester`
        """
        try:
            # Find the first ingester whose id matches
            return next(
                filter(lambda ingester: ingester.id == id, self.ingesters)
            )
        except StopIteration:
            raise IngesterNotFoundError(
                'Unable to find ingester with id {}'.format(id)
            )

    def where(self, options):
        """
        Finds ingesters that match the search criteria

        :param options: contains string:string key value pairs, allowed keys
                        are those found in the Ingester.SEARCH_FIELDS constant
        :type dict

        :return: A list of matching ingesters
        :rtype: :class:`IngesterList`
        """
        self._validate_search_options(options)

        # If options is empty, just return a new copy of the IngesterList
        if not options:
            return IngesterList(self.ingesters)

        # Create a lambda that will check to see if all the values in the
        # dictionary are found in the corresponding attributes of the ingester
        #
        # i.e. If options = { "name": "apple", "description": "banana" }, the
        #      lambda will check that "apple" is in ingester.name and "banana"
        #      is in ingester.description - both conditions would need to be met
        #      in order for the lambda to return True
        match_lambda = lambda ingester: all(
            [value in getattr(ingester, key) for key, value in options.items()]
        )

        # Get a list of ingesters that match the search options
        ingester_matches = list(filter(match_lambda, self.ingesters))

        return IngesterList(ingester_matches)

    def _coerce_ingester(self, ingester):
        """
        Helper method to ensure all members of the ingesters list are instances
        of Ingester

        :param ingester: either the dict or Ingester form of the ingester
        :type ingester: Union[dict, :class:`Ingester`]

        :return: an instance of Ingester
        :rtype :class:`Ingester`
        """
        # Return the original ingester if it is already an instance of Ingester
        return ingester if isinstance(ingester, Ingester) else Ingester(ingester)

    def _validate_search_options(self, options):
        if not isinstance(options, dict):
            raise TypeError(
                'Expected options to be of type dict, got {}'.format(
                    options.__class__
                )
            )

        # Check that the search keys are all valid
        [Ingester.validate_search_key(key, False) for key in options]
