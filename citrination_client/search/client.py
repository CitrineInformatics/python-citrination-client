from .query_encoder import QueryEncoder
from citrination_client.search import *
from pypif.util.case import to_camel_case
from pypif.util.case import keys_to_snake_case

from citrination_client.base.base_client import BaseClient
from copy import deepcopy
import json
import requests

class SearchClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        self.pif_search_endpoint = 'search/pif_search'
        self.pif_multi_search_endpoint = 'search/pif/multi_pif_search'
        self.dataset_search_endpoint = 'search/dataset'
        BaseClient.__init__(self, api_key, webserver_host="https://citrination.com")

    def search(self, pif_system_returning_query):
        """
        Run a PIF query against Citrination. This is just an alias for the pif_search method for backwards
        compatibility.

        :param pif_system_returning_query: :class:`PifSystemReturningQuery` to execute.
        :return: :class:`PifSearchResult` object with the results of the query.
        """
        return self.pif_search(pif_system_returning_query)

    def pif_search(self, pif_system_returning_query):
        """
        Run a PIF query against Citrination.

        :param pif_system_returning_query: :class:`PifSystemReturningQuery` to execute.
        :return: :class:`PifSearchResult` object with the results of the query.
        """
        if pif_system_returning_query.size is None and pif_system_returning_query.from_index is None:
            total = 1; time = 0.0; hits = []; first = True
            while len(hits) < min(total, 10000):
                if first:
                    first = False
                else:
                    sleep(3)
                sub_query = deepcopy(pif_system_returning_query)
                sub_query.from_index = len(hits)
                partial_results = self.pif_search(sub_query)
                total = partial_results.total_num_hits
                time += partial_results.took
                if partial_results.hits is not None:
                    hits.extend(partial_results.hits)
            return PifSearchResult(hits=hits, total_num_hits=total, took=time)

        response = self._post(
            self.pif_search_endpoint, data=json.dumps(pif_system_returning_query, cls=QueryEncoder),
          )
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifSearchResult(**keys_to_snake_case(response.json()['results']))

    def pif_multi_search(self, multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param multi_query: :class:`MultiQuery` object to execute.
        :return: :class:`PifMultiSearchResult` object with the results of the query.
        """
        print(self.pif_multi_search_endpoint)
        response = self._post(
            self.pif_multi_search_endpoint, data=json.dumps(multi_query, cls=QueryEncoder))
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifMultiSearchResult(**keys_to_snake_case(response.json()['results']))

    def dataset_search(self, dataset_returning_query):
        """
        Run a dataset query against Citrination.

        :param dataset_returning_query: :class:`DatasetReturningQuery` to execute.
        :return: :class:`DatasetSearchResult` object with the results of the query.
        """
        if dataset_returning_query.size is None and dataset_returning_query.from_index is None:
            total = 1; time = 0.0; hits = []; first = True
            while len(hits) < min(total, 10000):
                if first:
                    first = False
                else:
                    sleep(3)
                sub_query = deepcopy(dataset_returning_query)
                sub_query.from_index = len(hits)
                partial_results = self.dataset_search(sub_query)
                total = partial_results.total_num_hits
                time += partial_results.took
                if partial_results.hits is not None:
                    hits.extend(partial_results.hits)
            return DatasetSearchResult(hits=hits, total_num_hits=total, took=time)

        response = self._post(
            self.dataset_search_endpoint, data=json.dumps(dataset_returning_query, cls=QueryEncoder))
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return DatasetSearchResult(**keys_to_snake_case(response.json()['results']))

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
