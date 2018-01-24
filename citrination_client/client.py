import json
import os
from copy import deepcopy
from time import sleep

import requests

from citrination_client.search import *
from citrination_client.util.quote_finder import quote

from pypif.util.case import to_camel_case
from pypif.util.case import keys_to_snake_case


class CitrinationClient(object):
    """
    Class for interacting with the Citrination api.
    """

    def __init__(self, api_key, site='https://citrination.com', proxies=None):
        """
        Constructor.

        :param api_key: Authentication token.
        :param site: Specific site on citrination.com to work with. By default this client interacts with
        https://citrination.com. This should point to the full url of the site to access. For example, to access
        the STEEL site on citrination, use 'https://STEEL.citrination.com'.
        :param proxies: A map of proxies to use when making the request. For example, to proxy all https requests
        through https://myproxysite.com use {'https': 'https://myproxysite.com'}.
        """
        self.headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json', 'X-Citrination-API-Version': '1.0.0'}
        self.api_url = site + '/api'
        self.pif_search_url = self.api_url + '/search/pif_search'
        self.pif_multi_search_url = self.api_url + '/search/pif/multi_pif_search'
        self.dataset_search_url = self.api_url + '/search/dataset'
        self.proxies = proxies

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

        response = self._post_with_version_check(
            self.pif_search_url, data=json.dumps(pif_system_returning_query, cls=QueryEncoder),
            headers=self.headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifSearchResult(**keys_to_snake_case(response.json()['results']))

    def pif_multi_search(self, multi_query):
        """
        Run each in a list of PIF queries against Citrination.

        :param multi_query: :class:`MultiQuery` object to execute.
        :return: :class:`PifMultiSearchResult` object with the results of the query.
        """
        response = self._post_with_version_check(
            self.pif_multi_search_url, data=json.dumps(multi_query, cls=QueryEncoder), headers=self.headers)
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

        response = self._post_with_version_check(
            self.dataset_search_url, data=json.dumps(dataset_returning_query, cls=QueryEncoder), headers=self.headers)
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

    def predict(self, model_name, candidates, method="scalar", use_prior=True):
        """
        Predict endpoint

        :param model_name: The model identifier (id number for data views)
        :param candidates: A list of candidates to make predictions on
        :param method:     Method for propagating predictions through model graphs
        :param use_prior:  Whether to apply prior values implied by the property descriptors
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """
        body = self._get_predict_body(candidates, method, use_prior)

        url = self._get_predict_url(model_name)
        response = self._post_with_version_check(url, data=body, headers=self.headers)
        if response.status_code == 404:
            url = self._get_deprecated_predict_url(model_name)
            response = self._post_with_version_check(url, data=body, headers=self.headers)

        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))

        return response.json()

    def predict_custom(self, model_path, candidates):
        """
        Predict endpoint for a custom model

        :param model_path: The path from the custom model url (https://citrination.com/predict/{{model_path}})
        :param candidates: A list of candidates to make predictions on
        :return: the response, containing a list of predicted candidates as a map {property: [value, uncertainty]}
        """

        body = self._get_predict_body(candidates)

        url = self._get_custom_predict_url(model_path)
        response = self._post_with_version_check(url, data=body, headers=self.headers)

        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))

        return response.json()

    def _get_predict_body(self, candidates, method="scalar", use_prior=True):
        if not (method == "scalar" or method == "from_distribution"):
            raise ValueError("{} method not supported".format(method))

        # If a single candidate is passed, wrap in a list for the user
        if not isinstance(candidates, list):
            candidates = [candidates]

        return json.dumps(
            {"predictionRequest": {"predictionSource": method, "usePrior": use_prior, "candidates": candidates}},
            cls=QueryEncoder)

    def _get_custom_predict_url(self, model_path):
        return self.api_url + '/ml_templates/' + model_path + '/predict'

    def _get_predict_url(self, model_name):
        return self.api_url + '/data_views/' + model_name + '/predict'

    def _get_deprecated_predict_url(self, model_name):
        return self.api_url + '/csv_to_models/' + model_name + '/predict'

    def upload(self, dataset_id, source_path, dest_path=None):
        """
        Upload a file, specifying source and dest paths a file (acts as the scp command)
        :param source_path: The path to the file on the source host
        :param dest_path: The path to the file where the contents of the upload will be written (on the dest host)
        :return: A JSON block with a "message" key indicating that the upload if files is complete:
                {
                    "message": "Upload of files is complete.",
                    "successes": List of filepaths which were uploaded successfully,
                    "failures": List of filepaths which failed to upload
                }
        """
        source_path = str(source_path)
        if not dest_path:
            dest_path = source_path
        else:
            dest_path = str(dest_path)

        if os.path.isdir(source_path):
            successes = []
            failures = []
            for path, subdirs, files in os.walk(source_path):
                for name in files:
                    path_without_root_dir = path.split("/")[1:] + [name]
                    current_dest_path = os.path.join(dest_path, *path_without_root_dir)
                    current_source_path = os.path.join(path, name)
                    result = json.loads(self.upload(dataset_id, current_source_path, current_dest_path))
                    if result["success"]:
                        successes.append(current_source_path)
                    else:
                        failures.append(current_source_path)
            message = {
                "message": "Upload of files is complete.",
                "successes": successes,
                "failures": failures
            }
            return json.dumps(message)
        elif os.path.isfile(source_path):
            url = self._get_upload_url(dataset_id)
            file_data = { "dest_path": str(dest_path), "src_path": str(source_path)}
            r = self._post_with_version_check(url, data=json.dumps(file_data), headers=self.headers)
            if r.status_code == 200:
                j = json.loads(r.content.decode('utf-8'))
                s3url = self._get_s3_presigned_url(j)
                with open(source_path, 'rb') as f:
                    r = requests.put(s3url, data=f, headers=j["required_headers"], proxies=self.proxies)
                    if r.status_code == 200:
                        url_data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                        self._post_with_version_check(self._get_update_file_upload_url(j['file_id']),
                                      data=json.dumps(url_data), headers=self.headers)
                        message = {"message": "Upload is complete.",
                                   "data_set_id": str(dataset_id),
                                   "version": j['dataset_version_id'],
                                   "success": True}
                        return json.dumps(message)
                    else:
                        message = {"message": "Upload failed.",
                                   "status": r.status_code,
                                   "success": False}
                        return json.dumps(message)
            else:
                message = {"message": "Upload failed.",
                                   "status": r.status_code,
                                   "success": False}
                return json.dumps(message)
        else:
            return json.dumps({
                    "message": "No file at specified path {0}".format(source_path),
                    "success": False
                })

    def upload_file(self, file_path, dataset_id, root_path=None):
        """
        Upload file to Citrination.
        :param file_path: File path to upload.
        :param data_set_id: The dataset id to upload the file to.
        :return: Response object or return code if the file was not uploaded.
        """
        return self.upload(dataset_id, file_path)

    def _data_analysis(self, model_name):
        """
        Data analysis endpoint
        :param model_name: The model identifier (id number for data views)
        :return: dictionary containing information about the data, e.g. dCorr and tsne
        """
        url = self._get_data_analysis_url(model_name)
        return self._get_content_from_url(url)

    def tsne(self, model_name):
        """
        Get the t-SNE projection, including z-values and labels
        :param model_name: The model identifier (id number for data views)
        :return: dictionary containing property names and the projection for each
        """
        analysis = self._data_analysis(model_name)
        projections = analysis['projections']
        cleaned = {}
        for k, v in projections.items():
            d = {}
            d['x'] = v['x']
            d['y'] = v['y']
            d['z'] = v['label']
            d['label'] = v['inputs']
            d['uid'] = v['uid']
            cleaned[k] = d

        return cleaned

    def list_files(self, dataset_id, glob=".", is_dir=False):
        """
        List matched filenames in a dataset on Citrination.
        :param dataset_id: The ID of the dataset to search for files.
        :param glob: A pattern which will be matched against files in the dataset.
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :return: Response object or return code if the file was not uploaded.
        """
        url = self.api_url + '/datasets/' + str(dataset_id) + '/list_filepaths'
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        r = self._post_with_version_check(url, data=json.dumps(data), headers=self.headers)
        return json.loads(r.content.decode('utf-8'))

    def matched_file_count(self, dataset_id, glob=".", is_dir=False):
        list_result = self.list_files(dataset_id, glob, is_dir)
        if isinstance(list_result["files"], list):
            return len(list_result["files"])
        else:
            return list_result

    def get_matched_dataset_files(self, dataset_id, glob, is_dir=False, latest=True):
        """
        Retrieves URLs for the files matched by a glob or a path to a directory
        in a given dataset.

        :param dataset_id: The id of the dataset to retrieve files from
        :param glob: A regex used to select one or more files in the dataset
        :param is_dir: A flag used to indicate that the glob should be matched against the start of the paths in the dataset (simulates directory matching)
        :param latest: A boolean flag indicating that results should be limited to reporting files from the latest dataset version
        :return: The response object, or an error message object if the request failed
        """
        data = {
            "download_request": {
                "glob": glob,
                "isDir": is_dir,
                "latest": latest
            }
        }
        url = self.api_url + '/datasets/' + str(dataset_id) + '/download_files'
        r = self._post_with_version_check(url,data=json.dumps(data), headers=self.headers)
        return json.loads(r.content.decode('utf-8'))


    def get_dataset_files(self, dataset_id, latest = False):
        """
        Retrieves URLs for the files contained in a given dataset.

        :param data_set_id: The id of the dataset to retrieve files from
        :param latest: A boolean flag indicating that results should be limited to reporting files from the latest dataset version
        :return: The response object, or an error message object if the request failed
        """
        if isinstance(latest, bool):
            return self.get_matched_dataset_files(dataset_id, ".", False, latest)
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
            return self._get_content_from_url(self.api_url + '/datasets/' + str(dataset_id) + '/file/' + quote(file_path))
        else:
            return self._get_content_from_url(self.api_url + '/datasets/' + str(dataset_id) + '/version/' + str(version) + '/files/' + quote(file_path))

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
        result = requests.get(url, headers=self.headers, proxies=self.proxies)
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

    def _get_with_version_check(self, url, headers):
        result = requests.get(url, headers=headers, proxies=self.proxies)
        return self._check_response_for_version_mismatch(result)

    def _post_with_version_check(self, url, data, headers):
        result = requests.post(url, headers=headers, data=data, proxies=self.proxies)
        return self._check_response_for_version_mismatch(result)

    def _put_with_version_check(self, url, data, headers):
        result = requests.put(url, data=data, headers=headers, proxies=self.proxies)
        return self._check_response_for_version_mismatch(result)

    def _check_response_for_version_mismatch(self, response):
        response_content = json.loads(response.content.decode('utf-8'))
        try:
            if response.status_code == 400:
                error_type = response_content["error_type"]
                if error_type == "Version Mismatch":
                    print("Version mismatch with Citrination identified. Please check for available PyCC updates")
                    return False
            return response
        except KeyError:
            return response

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
        return self._post_with_version_check(url, headers=self.headers, data=json.dumps(dataset))

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
        return self._post_with_version_check(url, headers=self.headers, data=json.dumps(dataset))

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
        return self._post_with_version_check(url, headers=self.headers, data=json.dumps({}))

    def _get_create_data_set_version_url(self, data_set_id):
        """
        Helper method to generate the url for creating a new data set version.

        :return: URL for creating new data set versions.
        """
        return self.api_url+'/data_sets/'+str(data_set_id)+'/create_dataset_version'

    def _get_data_analysis_url(self, model_name):
        return self.api_url + '/data_views/' + model_name + '/data_analysis'


class QueryEncoder(json.JSONEncoder):
    """
    Class used to convert a query to json.
    """

    def default(self, obj):
        """
        Convert an object to a form ready to dump to json.

        :param obj: Object being serialized. The type of this object must be one of the following: None; a single
        object derived from the Pio class; or a list of objects, each derived from the Pio class.
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
        Make a copy of a dictionary with all keys converted to camel case. This is just calls to_camel_case on
        each of the keys in the dictionary and returns a new dictionary.

        :param obj: Dictionary to convert keys to camel case.
        :return: Dictionary with the input values and all keys in camel case
        """
        return dict((to_camel_case(key), value) for (key, value) in obj.items())
