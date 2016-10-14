import json
import requests
from pypif import pif
from pypif.util.case import keys_to_snake_case
from citrination_client.util.quote_finder import quote
from citrination_client.search.pif.result.pif_search_result import PifSearchResult


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

    def search(self, pif_query):
        """
        Run a PIF query against Citrination.

        :param pif_query: :class:`.PifQuery` to execute.
        :return: :class:`.PifSearchResult` object with the results of the query.
        """
        response = requests.post(self.pif_search_url, data=pif.dumps(pif_query), headers=self.headers)
        if response.status_code != requests.codes.ok:
            raise RuntimeError('Received ' + str(response.status_code) + ' response: ' + str(response.reason))
        return PifSearchResult(**keys_to_snake_case(response.json()['results']))

    def upload_file(self, file_path, data_set_id):
        """
        Upload file to Citrination.

        :param file_path: File path to upload.
        :param data_set_id: The dataset id to upload the file to.
        :return: Response object or None if the file was not uploaded.
        """
        url = self._get_upload_url(data_set_id)
        file_data = {"file_path": str(file_path)}
        r = requests.post(url, data=json.dumps(file_data), headers=self.headers)
        if r.status_code == 200:
            j = json.loads(r.content)
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
            return None

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
        print(str(url))
        result = requests.get(url, headers=self.headers)
        if result.status_code == 200:
            return json.loads(result.content)
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

    def create_data_set(self):
        """
        Create a new data set.

        :return: Response from the create data set request.
        """
        url = self._get_create_data_set_url()
        return requests.post(url, headers=self.headers)

    def _get_create_data_set_url(self):
        """
        Helper method to generate the url for creating a new data set.

        :return: URL for creating a new data set.
        """
        return self.api_url+'/data_sets/create_dataset'

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
