import urllib
import requests


class CitrinationClient(object):
    """
    Class for interacting with the Citrination api.
    """

    def __init__(self, api_key, site='https://citrination.com'):
        """
        Constructor.

        :param api_key: Authentication token.
        :type api_key: String

        :param site: Specific site on citrination.com to work with. By default this client interacts with
        https://citrination.com. This should point to the full url of the site to access.
        :type site: String
        """
        self.header = {'X-API-Key': urllib.quote(api_key), 'Content-Type': 'application/json'}
        self.api_url = site+'/api'

    def search(self, term=None, formula=None, contributor=None, reference=None, from_page=0,
               per_page=10, data_set_id=None):
        """
        Retrieve search results from Citrination. Searches are extremely inclusive and will include anything that
        contains anything found in the term argument.

        :param term: General search string. This is searched against all fields.
        :type term: String

        :param formula: Filter for the chemical formula field. Only those results that have chemical formulas that
        contain this string will be returned.
        :type formula: String

        :param contributor: Filter for the contributor field. Only those results that have contributors that contain
        this string will be returned.
        :type contributor: String

        :param reference: Filter for the reference field. Only those results that have contributors that contain
        this string will be returned.
        :type reference: String

        :param from_page: Index of the first page to return (indexed from 0).
        :type from_page: Integer

        :param per_page: Number of results to return.
        :type per_page: Integer

        :param data_set_id: Id of the particular data set to search on.
        :type data_set_id: Integer

        :return: Result of the requests.post method (see http://www.python-requests.org/en/latest). If the post returns
        a 200 message, then the search results can be converted to a python list/dictionary using the .json() method
        on the return object.
        """
        url = self._get_search_url(data_set_id)
        data = {'term': term, 'formula': formula, 'contributor': contributor,
                'reference': reference, 'from': from_page, 'per_page': per_page}
        response = requests.post(url, header=self.header, data=data)

    def _get_search_url(self, data_set_id):
        """
        Helper method to generate the url for search.

        :param data_set_id: Id of the particular data set to search on.
        :type data_set_id: Integer

        :return: String with the url for searching.
        """
        return self.api_url+'/mifs/search' if data_set_id is None else \
            self.api_url+'/datasets/'+str(data_set_id)+'/mifs/search'
