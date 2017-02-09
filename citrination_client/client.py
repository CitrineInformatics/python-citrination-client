import json
import os
import requests
from copy import deepcopy
from time import sleep
from pypif import pif
from pypif.util.case import keys_to_snake_case
from citrination_client.util.quote_finder import quote
from citrination_client.search.pif.query.pif_query import PifQuery
from citrination_client.search.pif.query.core.field_operation import FieldOperation
from citrination_client.search.pif.query.core.filter import Filter
from citrination_client.search.pif.query.core.property_query import PropertyQuery
from citrination_client.search.pif.query.core.reference_query import ReferenceQuery
from citrination_client.search.pif.query.core.system_query import SystemQuery
from citrination_client.search.pif.query.chemical.chemical_field_operation import  ChemicalFieldOperation
from citrination_client.search.pif.query.chemical.chemical_filter import ChemicalFilter
from citrination_client.search.pif.result.pif_search_result import PifSearchResult
from citrination_client.search.pif.result.pif_multi_search_result import PifMultiSearchResult


class CitrinationClient(object):
    """
    Class for interacting with the Citrination api.
    """

    def __init__(self, api_key, site='https://citrination.com'):
        """
        Constructor.

        :param api_key: Authentication token.
        :param site: Specific site on citrination.com to work with. By default this client interacts with
        https://citrination.com. This should point to the full url of the site to access. For example, to access
        the STEEL site on citrination, use 'https://STEEL.citrination.com'.
        """
        self.headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json'}
        self.api_url = site + '/api'
        self.pif_search_url = self.api_url + '/search/pif_search'
        self.pif_multi_search_url = self.api_url + '/search/pif_multi_search'

    def search(self, pif_query):
        """
        Run a PIF query against Citrination.

        :param pif_query: :class:`.PifQuery` to execute.
        :return: :class:`.PifSearchResult` object with the results of the query.
        """
        if pif_query.size is None and pif_query.from_index is None:
            total = 1; time = 0.0; hits = []; first = True
            while len(hits) < min(total, 10000):
                if first:
                    first = False
                else:
                    sleep(3)
                sub_query = deepcopy(pif_query)
                sub_query.from_index = len(hits)
                partial_results = self.search(sub_query)
                total = partial_results.total_num_hits
                time += partial_results.took
                if partial_results.hits is not None:
                    hits.extend(partial_results.hits)
            return PifSearchResult(hits=hits, total_num_hits=total, took=time)

        response = requests.post(self.pif_search_url, data=pif.dumps(pif_query), headers=self.headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifSearchResult(**keys_to_snake_case(response.json()['results']))

    def pif_multi_search(self, pif_multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param pif_multi_query: :class:`.PifMultiQuery` object to execute.
        :return: :class:`.PifMultiSearchResult` object with the results of the query.
        """
        response = requests.post(self.pif_multi_search_url, data=pif.dumps(pif_multi_query), headers=self.headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifMultiSearchResult(**keys_to_snake_case(response.json()['results']))

    def simple_chemical_search(self, name=None, chemical_formula=None, property_name=None, property_value=None,
                               property_min=None, property_max=None, property_units=None, reference_doi=None,
                               include_datasets=[], exclude_datasets=[], from_index=None, size=None):
        """
        Run a query against Citrination. This method generates a :class:`.PifQuery` object using the supplied arguments.
        All arguments that accept lists have logical OR's on the queries that they generate. This means that, for
        example, simple_chemical_search(name=['A', 'B']) will match records that have name equal to 'A' or 'B'.

        Results will be pulled into the extracted field of the :class:`.PifSearchHit` objects that are returned. The
        name will appear under the key "name", chemical formula under "chemical_formula", property name under
        "property_name", value of the property under "property_value", units of the property under "property_units",
        and reference DOI under "reference_doi".

        This method is only meant for execution of very simple queries. More complex queries must use the search method
        that accepts a :class:`.PifQuery` object.

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
        :return: :class:`.PifSearchResult` object with the results of the query.
        """
        system_query = SystemQuery()
        system_query.names = FieldOperation(
            extract_as='name',
            filter=[Filter(equal=i) for i in self._get_list(name)])
        system_query.chemical_formula = ChemicalFieldOperation(
            extract_as='chemical_formula',
            filter=[ChemicalFilter(equal=i) for i in self._get_list(chemical_formula)])
        system_query.references = ReferenceQuery(doi=FieldOperation(
            extract_as='reference_doi',
            filter=[Filter(equal=i) for i in self._get_list(reference_doi)]))

        # Generate the parts of the property query
        property_name_query = FieldOperation(
            extract_as='property_name',
            filter=[Filter(equal=i) for i in self._get_list(property_name)])
        property_units_query = FieldOperation(
            extract_as='property_units',
            filter=[Filter(equal=i) for i in self._get_list(property_units)])
        property_value_query = FieldOperation(
            extract_as='property_value',
            filter=[])
        for i in self._get_list(property_value):
            property_value_query.filter.append(Filter(equal=i))
        if property_min is not None or property_max is not None:
            property_value_query.filter.append(Filter(min=property_min, max=property_max))

        # Generate the full property query
        system_query.properties = PropertyQuery(
            name=property_name_query,
            value=property_value_query,
            units=property_units_query)

        # Run the query
        query = PifQuery(
            system=system_query,
            from_index=from_index,
            size=size,
            score_relevance=True,
            include_datasets=include_datasets,
            exclude_datasets=exclude_datasets)
        return self.search(query)

    @staticmethod
    def _get_list(values):
        """
        Helper method that wraps values in a list. If the input is a list then it is returned. If the input is None
        then an empty list is returned. For anything else, the input value is wrapped as a single-element list.

        :param values: Value to make sure exists in a list.
        :return: List with the input values.
        """
        if values is None:
            return []
        elif isinstance(values, list):
            return values
        else:
            return [values]

    def predict(self, model_name, candidates):
        """
        Predict endpoint
        :param model_name: The model path
        :param candidates: A list of candidates
        :return: list of predicted candidates as a map {property: [value, uncertainty]}
        """

        # If a single candidate is passed, wrap in a list for the user
        if not isinstance(candidates, list):
            candidates = [candidates]

        url = self._get_predict_url(model_name)
        body = pif.dumps(
            {"predictionRequest": {"predictionSource": "scalar", "usePrior": True, "candidates": candidates}}
        )

        response = requests.post(url, data=body, headers=self.headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))

        return response.json()

    def _get_predict_url(self, model_name):
        return self.api_url + '/csv_to_models/' + model_name + '/predict'

    def upload_file(self, file_path, data_set_id, root_path=None):
        """
        Upload file to Citrination.

        :param file_path: File path to upload.
        :param data_set_id: The dataset id to upload the file to.
        :return: Response object or return code if the file was not uploaded.
        """
        if os.path.isdir(str(file_path)):
            for path, subdirs, files in os.walk(file_path):
                for name in files:
                    if root_path:
                       root = root_path
                    else:
                       root = str(file_path)
                    success = self.upload_file(os.path.join(path, name), data_set_id, root)
                    print(success)
            message = {"message": "Upload of files in " + str(root) + " is complete."}
            return json.dumps(message)
        else:
            url = self._get_upload_url(data_set_id)
            file_data = {"file_path": str(file_path)}
            if root_path:
                file_data["root_path"] = root_path

            r = requests.post(url, data=json.dumps(file_data), headers=self.headers)
            if r.status_code == 200:
                j = json.loads(r.content.decode('utf-8'))
                s3url = self._get_s3_presigned_url(j)
                with open(file_path, 'rb') as f:
                    r = requests.put(s3url, data=f)
                    if r.status_code == 200:
                        url_data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                        requests.post(self._get_update_file_upload_url(j['file_id']),
                                      data=json.dumps(url_data), headers=self.headers)
                        message = {"message": "Upload is complete.",
                                   "data_set_id": str(data_set_id),
                                   "version": j['dataset_version_id']}
                        return json.dumps(message)
                    else:
                        message = {"message": "Upload failed.",
                                   "status": r.status_code}
                        return json.dumps(message)
            else:
                message = {"message": "Upload failed.",
                                   "status": r.status_code}
                return json.dumps(message)

    def get_dataset_files(self, dataset_id, latest = False):
        """
        Retrieves URLs for the files contained in a given dataset.

        :param data_set_id: The id of the dataset to retrieve files from
        :param latest: A boolean flag indicating that results should be limited to reporting files from the latest dataset version
        :return: The response object, or an error message object if the request failed
        """
        if latest == False:
            return self._get_content_from_url(self.api_url + '/data_sets/' + str(dataset_id) + '/files')
        elif latest == True:
            return self._get_content_from_url(self.api_url + '/data_sets/' + str(dataset_id) + '/latest')
        else:
            return {
                "message": "If provided, the second parameter must be a boolean"
            }


    def get_dataset_file(self, dataset_id, file_path, version = None):
        """
        Retrieves the URL for a file contained in a given dataset by version (optional) and filepath.

        :param data_set_id: The id of the dataset to retrieve file from
        :param file_path: The file path within the dataset
        :param version: The dataset version to look for the file in. If nothing is supplied, the latest dataset version will be searched
        :return: The response object, or an error message object if the request failed
        """
        if version == None:
            return self._get_content_from_url(self.api_url + '/data_sets/' + str(dataset_id) + '/file/' + quote(file_path))
        else:
            return self._get_content_from_url(self.api_url + '/data_sets/' + str(dataset_id) + '/version/' + str(version) + '/files/' + quote(file_path))

    def get_pif(self, dataset_id, uid, version = None):
        """
        Retrieves JSON representation of a PIF from a given dataset.

        :param data_set_id: The id of the dataset to retrieve PIF from
        :param uid: The uid of the PIF to retrieve
        :param version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :return: The response object, or an error message object if the request failed
        """
        if version == None:
            return self._get_content_from_url(self.api_url + '/datasets/' + str(dataset_id) + '/pif/' + str(uid))
        else:
            return self._get_content_from_url(self.api_url + '/datasets/' + str(dataset_id) + '/version/' + str(version) + '/pif/' + str(uid))

    def _get_content_from_url(self, url):
        """
        Helper method to make get request to a URL.

        :param url: The URL to make the GET request to
        :return: The response object, or an error message object if the request failed
        """
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return json.loads(result.content.decode('utf-8'))
        else:
            print('An error ocurred during this action: ' + str(result.status_code) + ' - ' + str(result.reason) )
            return False

    def _get_upload_url(self, data_set_id):
        """
        Helper method to generate the url for file uploading.

        :param data_set_id: Id of the particular data set to upload to.
        :return: String with the url for uploading to Citrination.
        """
        return self.api_url+'/data_sets/'+str(data_set_id)+'/upload'

    @staticmethod
    def _get_s3_presigned_url(input_json):
        """
        Helper method to create an S3 presigned url from the json.
        """
        url = input_json['url']
        return url['scheme']+'://'+url['host']+url['path']+'?'+url['query']

    def _get_update_file_upload_url(self, file_id):
        """
        Helper method to generate the url for updating the file record with the upload bucket path

        :param file_id: Id of the file record.
        :type file_id: Integer

        :return: String with the url for uploading directly to S3
        """
        return self.api_url+'/data_sets/update_file/'+str(file_id)

    def create_data_set(self, name=None, description=None, share=None):
        """
        Create a new data set.
        :param name: name of the dataset
        :param description: description for the dataset
        :param share: share the dataset with everyone on the site. Valid values are '1' or '0'.
                      1 means share with everyone on the site. 0 means only the owner of the dataset
                      can see the dataset.

        :return: Response from the create data set request.
        """
        url = self._get_create_data_set_url()
        data = {}
        data["public"] = '0'
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if share:
            data["public"] = share
        dataset = {"dataset": data}
        return requests.post(url, headers=self.headers, data=json.dumps(dataset))

    def _get_create_data_set_url(self):
        """
        Helper method to generate the url for creating a new data set.

        :return: URL for creating a new data set.
        """
        return self.api_url+'/data_sets/create_dataset'

    def update_data_set(self, data_set_id, name=None, description=None, share=None):
        """
        Update a data set.
        :param data_set_id:
        :param name: name of the dataset
        :param description: description for the dataset
        :param share: share the dataset with everyone on the site. Valid values are '1' or '0'.
                      1 means share with everyone on the site. 0 means only the owner of the dataset
                      can see the dataset.
        :return: Response from the update data set request.
        """
        url = self._get_update_data_set_url(data_set_id)
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if share:
            data["public"] = share
        dataset = {"dataset": data}
        return requests.post(url, headers=self.headers, data=json.dumps(dataset))

    def _get_update_data_set_url(self, data_set_id):
        """
        Helper method to generate the url for updating a data set.

        :return: URL for creating a new data set.
        """
        return self.api_url+'/data_sets/'+str(data_set_id)+'/update'

    def create_data_set_version(self, data_set_id):
        """
        Create a new data set version.

        :param data_set_id: Id of the particular data set to upload to.
        :return: Response from the create data set version request.
        """
        url = self._get_create_data_set_version_url(data_set_id)
        return requests.post(url, headers=self.headers)

    def _get_create_data_set_version_url(self, data_set_id):
        """
        Helper method to generate the url for creating a new data set version.

        :return: URL for creating new data set versions.
        """
        return self.api_url+'/data_sets/'+str(data_set_id)+'/create_dataset_version'
