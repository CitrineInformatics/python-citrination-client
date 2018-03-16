from .query_encoder import QueryEncoder
from pypif.util.case import to_camel_case
from pypif.util.case import keys_to_snake_case
from citrination_client.search import *
from citrination_client.util import config as client_config
from citrination_client.base.base_client import BaseClient
from citrination_client.util import http as http_util

from copy import deepcopy
from time import sleep
import json
import requests
import routes

class SearchClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        members = [
            "pif_search",
            "pif_multi_search",
            "dataset_search"
        ]
        super(SearchClient, self).__init__(api_key, webserver_host, members)

    def pif_search(self, pif_system_returning_query):
        """
        Run a PIF query against Citrination.

        :param pif_system_returning_query: :class:`PifSystemReturningQuery` to execute.
        :return: :class:`PifSearchResult` object with the results of the query.
        """
        return self._execute_paginating_search(
            pif_system_returning_query,
            PifSearchResult
        )

    def dataset_search(self, dataset_returning_query):
        """
        Run a dataset query against Citrination.

        :param dataset_returning_query: :class:`DatasetReturningQuery` to execute.
        :return: :class:`DatasetSearchResult` object with the results of the query.
        """
        return self._execute_paginating_search(
            dataset_returning_query,
            DatasetSearchResult
        )

    def _execute_paginating_search(self, returning_query, result_class):
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

        time = 0.0; hits = []; first = True
        while True:
            if first:
                first = False
            else:
                sleep(1)
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

        response_json = http_util.get_success_json(
                self._post(
                    route, data=json.dumps(returning_query, cls=QueryEncoder),
                ),
                failure_message
            )
        return result_class(**keys_to_snake_case(response_json['results']))

    def pif_multi_search(self, multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param multi_query: :class:`MultiQuery` object to execute.
        :return: :class:`PifMultiSearchResult` object with the results of the query.
        """
        response_json = http_util.get_success_json(
            self._post(
                routes.pif_multi_search, data=json.dumps(multi_query, cls=QueryEncoder)
            ),
            "Error while making PIF multi search request"
        )

        return PifMultiSearchResult(**keys_to_snake_case(response_json['results']))

    def simple_chemical_search(self, name=None, chemical_formula=None, property_name=None, property_value=None,
                               property_min=None, property_max=None, property_units=None, reference_doi=None,
                               include_datasets=[], exclude_datasets=[], from_index=None, size=None):
        """
        Run a query against Citrination. This method generates a :class:`PifSystemReturningQuery` object using the
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
        :param chemical_formula:  One or more strings with the chemical formulas to match.
        :param property_name: One or more strings with the names of the property to match.
        :param property_value: One or more strings or numbers with the exact values to match.
        :param property_min: A single string or number with the minimum value to match.
        :param property_max: A single string or number with the maximum value to match.
        :param property_units: One or more strings with the property units to match.
        :param reference_doi: One or more strings with the DOI to match.
        :param include_datasets: One or more integers with dataset IDs to match.
        :param exclude_datasets: One or more integers with dataset IDs that must not match.
        :param from_index: Index of the first record to match.
        :param size: Total number of records to return.
        :return: :class:`PifSearchResult` object with the results of the query.
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
        return self.pif_search(pif_system_returning_query)
