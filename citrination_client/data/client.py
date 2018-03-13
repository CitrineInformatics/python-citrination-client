from citrination_client.base.base_client import BaseClient
from citrination_client.errors import CitrinationClientError
import citrination_client.util.http as http_utils
import json
import os
import requests
import routes

class DataClient(BaseClient):

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        members = [
            "upload",
            "list_files",
            "matched_file_count",
            "get_matched_dataset_files",
            "get_dataset_files",
            "get_dataset_file",
            "create_dataset",
            "create_dataset_version"
        ]
        super(DataClient, self).__init__(api_key, webserver_host, members)

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
                    try:
                        self.upload(dataset_id, current_source_path, current_dest_path)
                        successes.append(current_source_path)
                    except (CitrinationClientError, ValueError):
                        failures.append(current_source_path)
            message = {
                "successes": successes,
                "failures": failures
            }
            return message
        elif os.path.isfile(source_path):
            file_data = { "dest_path": str(dest_path), "src_path": str(source_path)}
            r = self._post_json(routes.upload_to_dataset(dataset_id), data=file_data)
            if r.status_code == 200:
                j = r.json()
                s3url = _get_s3_presigned_url(j)
                with open(source_path, 'rb') as f:
                    r = requests.put(s3url, data=f, headers=j["required_headers"])
                    if r.status_code == 200:
                        data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                        self._post_json(routes.update_file(j['file_id']), data=data)
                        if r.status_code == 200:
                            return {
                                "successes": [source_path],
                                "failures": []
                            }
                        else:
                            raise CitrinationClientError("Failure to upload {} to Citrination".format(source_path))
                    else:
                        raise CitrinationClientError("Failure to upload {} to Citrination".format(source_path))
            else:
                raise CitrinationClientError("Failure to upload {} to Citrination".format(source_path))
        else:
            raise ValueError("No file at specified path {}".format(source_path))

    def list_files(self, dataset_id, glob=".", is_dir=False):
        """
        List matched filenames in a dataset on Citrination.
        :param dataset_id: The ID of the dataset to search for files.
        :param glob: A pattern which will be matched against files in the dataset.
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :return: Response object or return code if the file was not uploaded.
        """
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        return self._post_json(routes.list_files(dataset_id), data).json()

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
        response = self._post_json(routes.matched_files(dataset_id), data)
        failure_message = "Failed to get matched files in dataset {}".format(dataset_id)
        return http_utils.get_success_json(response, failure_message)

    def get_dataset_files(self, dataset_id, latest = False):
        """
        Retrieves URLs for the files contained in a given dataset.

        :param data_set_id: The id of the dataset to retrieve files from
        :param latest: A boolean flag indicating that results should be limited to reporting files from the latest dataset version
        :return: The response object, or an error message object if the request failed
        """
        result = self.get_matched_dataset_files(dataset_id, ".", False, latest)
        failure_message = "An error occurred retrieving files for dataset {}".format(dataset_id)
        return http_utils.get_success_json(result, failure_message)

    def get_dataset_file(self, dataset_id, file_path, version = None):
        """
        Retrieves the URL for a file contained in a given dataset by version (optional) and filepath.

        :param data_set_id: The id of the dataset to retrieve file from
        :param file_path: The file path within the dataset
        :param version: The dataset version to look for the file in. If nothing is supplied, the latest dataset version will be searched
        :return: The response object, or an error message object if the request failed
        """
        if version == None:
            result = self._get(routes.file_dataset_path(dataset_id, file_path))
        else:
            result = self._get(routes.file_dataset_version_path(dataset_id, version, file_path))

        return http_utils.get_success_json(result, "An error occurred retrieving file {}".format(file_path))


    def get_pif(self, dataset_id, uid, version = None):
        """
        Retrieves JSON representation of a PIF from a given dataset.

        :param data_set_id: The id of the dataset to retrieve PIF from
        :param uid: The uid of the PIF to retrieve
        :param version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :return: The response object, or an error message object if the request failed
        """
        if version == None:
            result = self._get(routes.pif_dataset_uid(dataset_id, uid))
        else:
            result = self._get(routes.pif_dataset_version_uid(dataset_id, uid, version))

        return http_utils.get_success_json(result, "An error occurred retrieving PIF {}".format(uid))

    def create_dataset(self, name=None, description=None, public=False):
        """
        Create a new data set.
        :param name: name of the dataset
        :param description: description for the dataset
        :param share: share the dataset with everyone on the site. Valid values are '1' or '0'.
                      1 means share with everyone on the site. 0 means only the owner of the dataset
                      can see the dataset.

        :return: Response from the create data set request.
        """
        data = {
            "public": _convert_bool_to_public_value(public)
        }
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        dataset = {"dataset": data}
        failure_message = "Unable to create dataset"
        result = self._post_json(routes.create_dataset(), dataset)
        return http_utils.get_success_json(result, failure_message)

    def update_dataset(self, dataset_id, name=None, description=None, public=None):
        """
        Update a data set.
        :param dataset_id:
        :param name: name of the dataset
        :param description: description for the dataset
        :param public: share the dataset with everyone on the site. Valid values are '1' or '0'.
                      1 means share with everyone on the site. 0 means only the owner of the dataset
                      can see the dataset.
        :return: Response from the update data set request.
        """
        data = {
            "public": _convert_bool_to_public_value(public)
        }

        if name:
            data["name"] = name
        if description:
            data["description"] = description

        dataset = {"dataset": data}
        return http_utils.get_success_json(
                self._post_json(routes.update_dataset(dataset_id), data=dataset),
                "Failed to update dataset {}".format(dataset_id)
            )

    def create_dataset_version(self, dataset_id):
        """
        Create a new data set version.

        :param dataset_id: Id of the particular data set to upload to.
        :return: Response from the create data set version request.
        """
        return http_utils.get_success_json(
                self._post_json(routes.create_dataset_version(dataset_id), data={}),
                "Failed to create dataset version for dataset {}".format(dataset_id)
            )

def _convert_bool_to_public_value(val):
    if val == None:
        return None
    if val == False:
        return '0'
    if val == True:
        return '1'

def _get_s3_presigned_url(input_json):
    """
    Helper method to create an S3 presigned url from the json.
    """
    url = input_json['url']
    return url['scheme']+'://'+url['host']+url['path']+'?'+url['query']