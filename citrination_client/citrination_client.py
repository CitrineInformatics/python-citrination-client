import json
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
        :param site: Specific site on citrination.com to work with. By default this client interacts with
        https://citrination.com. This should point to the full url of the site to access. For example, to access
        the STEEL site on citrination, use 'https://STEEL.citrination.com'.
        """
        self.headers = {'X-API-Key': urllib.quote(api_key), 'Content-Type': 'application/json'}
        self.api_url = site+'/api'

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
                    url_data = {'s3object': j['url']['path'], 's3bucket': j['bucket'] }
                    requests.post(self._get_update_file_upload_url(j['file_id']),
                                  data=json.dumps(url_data), headers=self.headers)
                    message = {"message":"Upload is complete.",
                               "data_set_id": str(data_set_id),
                               "version": j['dataset_version_id']}
                    return json.dumps(message)
                else:
                    message = {"message":"Upload failed.",
                               "status":r.status_code}
                    return json.dumps(message)
        else:
            return None

    def _get_upload_url(self, data_set_id):
        """
        Helper method to generate the url for file uploading.

        :param data_set_id: Id of the particular data set to upload to.
        :return: String with the url for uploading to Citrination.
        """
        return self.api_url+'/data_sets/'+str(data_set_id)+'/upload'

    def _get_s3_presigned_url(self, json):
        """
        Helper method to create an S3 presigned url from the json.
        """
        url = json['url']
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
