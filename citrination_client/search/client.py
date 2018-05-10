from citrination_client.search.query_encoder import QueryEncoder
from citrination_client.search import *
from citrination_client.search import routes as routes
from citrination_client.util import config as client_config
from citrination_client.base.base_client import BaseClient
from citrination_client.base.errors import RequestTimeoutException
from citrination_client.base.errors import CitrinationClientError

from pypif.util.case import to_camel_case
from pypif.util.case import keys_to_snake_case

from copy import deepcopy
import json
import requests

DEFAULT_FAILURE_MESSAGE = "An error occurred requesting search results from Citrination"
MAX_QUERY_DEPTH = 50000


class SearchClient(BaseClient):
    def __init__(self, api_key, webserver_host="https://citrination.com", suppress_warnings=False):
        members = [
            "pif_search",
            "pif_multi_search",
            "dataset_search"
        ]
        super(SearchClient, self).__init__(api_key, webserver_host, members, suppress_warnings=suppress_warnings)

    def _handle_response(self, response, failure_message=DEFAULT_FAILURE_MESSAGE):
        if response.status_code == 204:
            raise RequestTimeoutException()

        return super(SearchClient, self)._handle_response(response, failure_message)

    def _validate_search_query(self, returning_query):
        """
        Checks to see that the query will not exceed the max query depth

        :param returning_query: The PIF system or Dataset query to execute.
        :type returning_query: :class:`PifSystemReturningQuery` or :class: `DatasetReturningQuery`
        """

        start_index = returning_query.from_index or 0
        size = returning_query.size or 0

        if start_index < 0:
            raise CitrinationClientError(
                "start_index cannot be negative. Please enter a value greater than or equal to zero")
        if size < 0:
            raise CitrinationClientError("Size cannot be negative. Please enter a value greater than or equal to zero")
        if start_index + size > MAX_QUERY_DEPTH:
            raise CitrinationClientError(
                "Citrination does not support pagination past the {0}th result. Please reduce either the from_index and/or size such that their sum is below {0}".format(
                    MAX_QUERY_DEPTH))

    def pif_search(self, pif_system_returning_query):
        """
        Run a PIF query against Citrination.

        :param pif_system_returning_query: The PIF system query to execute.
        :type pif_system_returning_query: :class:`PifSystemReturningQuery`
        :return: :class:`PifSearchResult` object with the results of the query.
        :rtype: :class:`PifSearchResult`
        """

        self._validate_search_query(pif_system_returning_query)
        return self._execute_search_query(
            pif_system_returning_query,
            PifSearchResult
        )

    def dataset_search(self, dataset_returning_query):
        """
        Run a dataset query against Citrination.

        :param dataset_returning_query: :class:`DatasetReturningQuery` to execute.
        :type dataset_returning_query: :class:`DatasetReturningQuery`
        :return: Dataset search result object with the results of the query.
        :rtype: :class:`DatasetSearchResult`
        """

        self._validate_search_query(dataset_returning_query)
        return self._execute_search_query(
            dataset_returning_query,
            DatasetSearchResult
        )

    def _execute_search_query(self, returning_query, result_class):
        """
        Run a PIF query against Citrination.

        :param returning_query: :class:`BaseReturningQuery` to execute.
        :param result_class: The class of the result to return.
        :return: ``result_class`` object with the results of the query.
        """
        if returning_query.from_index:
            from_index = returning_query.from_index
        else:
            from_index = 0

        if returning_query.size != None:
            size = min(returning_query.size, client_config.max_query_size)
        else:
            size = client_config.max_query_size

        if (size == client_config.max_query_size and
                    size != returning_query.size):
            self._warn("Query size greater than max system size - only {} results will be returned".format(size))

        time = 0.0;
        hits = [];
        while True:
            sub_query = deepcopy(returning_query)
            sub_query.from_index = from_index + len(hits)
            partial_results = self._search_internal(sub_query, result_class)
            total = partial_results.total_num_hits
            time += partial_results.took
            if partial_results.hits is not None:
                hits.extend(partial_results.hits)
            if len(hits) >= size or len(hits) >= total or sub_query.from_index >= total:
                break

        return result_class(hits=hits, total_num_hits=total, took=time)

    def _search_internal(self, returning_query, result_class):
        if result_class == PifSearchResult:
            route = routes.pif_search
            failure_message = "Error while making PIF search request"

        elif result_class == DatasetSearchResult:
            route = routes.dataset_search
            failure_message = "Error while making dataset search request"

        response_json = self._get_success_json(self._post(
            route, data=json.dumps(returning_query, cls=QueryEncoder),
            failure_message=failure_message))

        return result_class(**keys_to_snake_case(response_json['results']))

    def pif_multi_search(self, multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param multi_query: :class:`MultiQuery` object to execute.
        :return: :class:`PifMultiSearchResult` object with the results of the query.
        """
        failure_message = "Error while making PIF multi search request"
        response_dict = self._get_success_json(
            self._post(routes.pif_multi_search, data=json.dumps(multi_query, cls=QueryEncoder),
                       failure_message=failure_message))

        return PifMultiSearchResult(**keys_to_snake_case(response_dict['results']))

    def generate_simple_chemical_query(self, name=None, chemical_formula=None, property_name=None, property_value=None,
                                       property_min=None, property_max=None, property_units=None, reference_doi=None,
                                       include_datasets=[], exclude_datasets=[], from_index=None, size=None):
        """
        This method generates a :class:`PifSystemReturningQuery` object using the
        supplied arguments. All arguments that accept lists have logical OR's on the queries that they generate.
        This means that, for example, simple_chemical_search(name=['A', 'B']) will match records that have name
        equal to 'A' or 'B'.

        Results will be pulled into the extracted field of the :class:`PifSearchHit` objects that are returned. The
        name will appear under the key "name", chemical formula under "chemical_formula", property name under
        "property_name", value of the property under "property_value", units of the property under "property_units",
        and reference DOI under "reference_doi".

        This method is only meant for execution of very simple queries. More complex queries must use the search method
        that accepts a :class:`PifSystemReturningQuery` object.

        :param name: One or more strings with the names of the chemical system to match.
        :type name: str or list of str
        :param chemical_formula:  One or more strings with the chemical formulas to match.
        :type chemical_formula: str or list of str
        :param property_name: One or more strings with the names of the property to match.
        :type property_name: str or list of str
        :param property_value: One or more strings or numbers with the exact values to match.
        :type property_value: str or int or float or list of str or int or float
        :param property_min: A single string or number with the minimum value to match.
        :type property_min: str or int or float
        :param property_max: A single string or number with the maximum value to match.
        :type property_max: str or int or float
        :param property_units: One or more strings with the property units to match.
        :type property_units: str or list of str
        :param reference_doi: One or more strings with the DOI to match.
        :type reference_doin: str or list of str
        :param include_datasets: One or more integers with dataset IDs to match.
        :type include_datasets: int or list of int
        :param exclude_datasets: One or more integers with dataset IDs that must not match.
        :type exclude_datasets: int or list of int
        :param from_index: Index of the first record to match.
        :type from_index: int
        :param size: Total number of records to return.
        :type size: int
        :return: A query to to be submitted with the pif_search method
        :rtype: :class:`PifSystemReturningQuery`
        """
        pif_system_query = PifSystemQuery()
        pif_system_query.names = FieldQuery(
            extract_as='name',
            filter=[Filter(equal=i) for i in self._get_list(name)])
        pif_system_query.chemical_formula = ChemicalFieldQuery(
            extract_as='chemical_formula',
            filter=[ChemicalFilter(equal=i) for i in self._get_list(chemical_formula)])
        pif_system_query.references = ReferenceQuery(doi=FieldQuery(
            extract_as='reference_doi',
            filter=[Filter(equal=i) for i in self._get_list(reference_doi)]))

        # Generate the parts of the property query
        property_name_query = FieldQuery(
            extract_as='property_name',
            filter=[Filter(equal=i) for i in self._get_list(property_name)])
        property_units_query = FieldQuery(
            extract_as='property_units',
            filter=[Filter(equal=i) for i in self._get_list(property_units)])
        property_value_query = FieldQuery(
            extract_as='property_value',
            filter=[])
        for i in self._get_list(property_value):
            property_value_query.filter.append(Filter(equal=i))
        if property_min is not None or property_max is not None:
            property_value_query.filter.append(Filter(min=property_min, max=property_max))

        # Generate the full property query
        pif_system_query.properties = PropertyQuery(
            name=property_name_query,
            value=property_value_query,
            units=property_units_query)

        # Generate the dataset query
        dataset_query = list()
        if include_datasets:
            dataset_query.append(DatasetQuery(logic='MUST', id=[Filter(equal=i) for i in include_datasets]))
        if exclude_datasets:
            dataset_query.append(DatasetQuery(logic='MUST_NOT', id=[Filter(equal=i) for i in exclude_datasets]))

        # Run the query
        pif_system_returning_query = PifSystemReturningQuery(
            query=DataQuery(
                system=pif_system_query,
                dataset=dataset_query),
            from_index=from_index,
            size=size,
            score_relevance=True)

        return pif_system_returning_query

    @staticmethod
    def _get_list(values):
        """
        Helper method that wraps values in a list. If the input is a list then it is returned. If the input is None then an empty list is returned. For anything else, the input value is wrapped as a single-element list.
        
        :param values: Value to make sure exists in a list.
        :return: List with the input values.
        """
        if values is None:
            return []
        elif isinstance(values, list):
            return values
        else:
            return [values]
