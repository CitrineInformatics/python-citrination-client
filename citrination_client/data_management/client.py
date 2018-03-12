from citrination_client.base.base_client import BaseClient
import json
import os
import requests

class DataManagementClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        members = [
            "upload",
            "list_files",
            "matched_file_count",
            "get_matched_dataset_files",
            "get_dataset_files",
            "get_dataset_file",
            "create_data_set",
            "create_data_set_version"
        ]
        super(DataManagementClient, self).__init__(api_key, webserver_host, members)

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
                    result = self.upload(dataset_id, current_source_path, current_dest_path)
                    if result["success"]:
                        successes.append(current_source_path)
                    else:
                        failures.append(current_source_path)
            message = {
                "message": "Upload of files is complete.",
                "successes": successes,
                "failures": failures
            }
            return message
        elif os.path.isfile(source_path):
            url = self._get_upload_url(dataset_id)
            file_data = { "dest_path": str(dest_path), "src_path": str(source_path)}
            r = self._post_json(url, data=file_data)
            if r.status_code == 200:
                j = r.json()
                s3url = self._get_s3_presigned_url(j)
                with open(source_path, 'rb') as f:
                    r = requests.put(s3url, data=f, headers=j["required_headers"])
                    if r.status_code == 200:
                        data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                        endpoint = 'data_sets/update_file/' + str(j['file_id'])
                        self._post_json(endpoint, data=data)
                        return {"message": "Upload is complete.",
                                   "data_set_id": str(dataset_id),
                                   "version": j['dataset_version_id'],
                                   "success": True}
                    else:
                        return {"message": "Upload failed.",
                                   "status": r.status_code,
                                   "success": False}
            else:
                return {"message": "Upload failed.",
                                   "status": r.status_code,
                                   "success": False}
        else:
            return {
                    "message": "No file at specified path {0}".format(source_path),
                    "success": False
                }

    def list_files(self, dataset_id, glob=".", is_dir=False):
        """
        List matched filenames in a dataset on Citrination.
        :param dataset_id: The ID of the dataset to search for files.
        :param glob: A pattern which will be matched against files in the dataset.
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :return: Response object or return code if the file was not uploaded.
        """
        endpoint = 'datasets/' + str(dataset_id) + '/list_filepaths'
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        return self._post_json(endpoint, data).json()

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
        endpoint = 'datasets/' + str(dataset_id) + '/download_files'
        return self._post_json(endpoint, data).json()

    def get_dataset_files(self, dataset_id, latest = False):
        """
        Retrieves URLs for the files contained in a given dataset.

        :param data_set_id: The id of the dataset to retrieve files from
        :param latest: A boolean flag indicating that results should be limited to reporting files from the latest dataset version
        :return: The response object, or an error message object if the request failed
        """
        if isinstance(latest, bool):
            return self.get_matched_dataset_files(dataset_id, ".", False, latest).json()
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
            return self._get('datasets/' + str(dataset_id) + '/file/' + quote(file_path)).json()
        else:
            return self._get('datasets/' + str(dataset_id) + '/version/' + str(version) + '/files/' + quote(file_path)).json()

    def get_pif(self, dataset_id, uid, version = None):
        """
        Retrieves JSON representation of a PIF from a given dataset.

        :param data_set_id: The id of the dataset to retrieve PIF from
        :param uid: The uid of the PIF to retrieve
        :param version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :return: The response object, or an error message object if the request failed
        """
        if version == None:
            return self._get('datasets/' + str(dataset_id) + '/pif/' + str(uid)).json()
        else:
            return self._get('datasets/' + str(dataset_id) + '/version/' + str(version) + '/pif/' + str(uid)).json()

    def _get_upload_url(self, data_set_id):
        """
        Helper method to generate the url for file uploading.

        :param data_set_id: Id of the particular data set to upload to.
        :return: String with the url for uploading to Citrination.
        """
        return 'data_sets/'+str(data_set_id)+'/upload'


    @staticmethod
    def _get_s3_presigned_url(input_json):
        """
        Helper method to create an S3 presigned url from the json.
        """
        url = input_json['url']
        return url['scheme']+'://'+url['host']+url['path']+'?'+url['query']

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
        endpoint = 'data_sets/create_dataset'
        data = {}
        data["public"] = '0'
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if share:
            data["public"] = share
        dataset = {"dataset": data}
        return self._post_json(endpoint, dataset).json()

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
        return self._post_json(url, data=json.dumps(dataset)).json()

    def _get_update_data_set_url(self, data_set_id):
        """
        Helper method to generate the url for updating a data set.

        :return: URL for creating a new data set.
        """
        return 'data_sets/'+str(data_set_id)+'/update'

    def create_data_set_version(self, data_set_id):
        """
        Create a new data set version.

        :param data_set_id: Id of the particular data set to upload to.
        :return: Response from the create data set version request.
        """
        url = self._get_create_data_set_version_url(data_set_id)
        return self._post_json(url, data=json.dumps({}))

    def _get_create_data_set_version_url(self, data_set_id):
        """
        Helper method to generate the url for creating a new data set version.

        :return: URL for creating new data set versions.
        """
        return 'data_sets/'+str(data_set_id)+'/create_dataset_version'