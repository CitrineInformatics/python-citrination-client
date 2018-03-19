from citrination_client.base.base_client import BaseClient
from citrination_client.errors import CitrinationClientError
from pypif import pif
from .upload_result import UploadResult
from .dataset import Dataset
from .dataset_file import DatasetFile
import citrination_client.util.http as http_utils
import json
import os
import requests
import routes

class DataClient(BaseClient):
    """
    Client encapsulating data management behavior.
    """

    def __init__(self, api_key, webserver_host="https://citrination.com"):
        """
        Constructor.

        :param api_key: A users API key, as a string
        :param webserver_host: The root site Url
        """
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
        :return: A :class:`UploadResult` object summarizing the result of
            the upload process
        """
        upload_result = UploadResult()
        source_path = str(source_path)
        if not dest_path:
            dest_path = source_path
        else:
            dest_path = str(dest_path)
        if os.path.isdir(source_path):
            for path, subdirs, files in os.walk(source_path):
                for name in files:
                    path_without_root_dir = path.split("/")[-1:] + [name]
                    current_dest_path = os.path.join(dest_path, *path_without_root_dir)
                    current_source_path = os.path.join(path, name)
                    try:
                        if self.upload(dataset_id, current_source_path, current_dest_path).successful():
                            upload_result.add_success(current_source_path)
                        else:
                            upload_result.add_failure(current_source_path,"Upload failure")
                    except (CitrinationClientError, ValueError) as e:
                        upload_result.add_failure(current_source_path, e.message)
            return upload_result
        elif os.path.isfile(source_path):
            file_data = { "dest_path": str(dest_path), "src_path": str(source_path)}
            j = self._post_json(routes.upload_to_dataset(dataset_id), data=file_data).json()
            s3url = _get_s3_presigned_url(j)
            with open(source_path, 'rb') as f:
                r = requests.put(s3url, data=f, headers=j["required_headers"])
                if r.status_code == 200:
                    data = {'s3object': j['url']['path'], 's3bucket': j['bucket']}
                    self._post_json(routes.update_file(j['file_id']), data=data)
                    upload_result.add_success(source_path)
                    return upload_result
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
        :return: A list of filepaths in the dataset matching the provided glob.
        """
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        return http_utils.get_success_json(
            self._post_json(routes.list_files(dataset_id), data),
            "Failed to list files for dataset {}".format(dataset_id)
        )['files']

    def matched_file_count(self, dataset_id, glob=".", is_dir=False):
        """
        Returns the number of files matching a pattern in a dataset
        :param dataset_id: The ID of the dataset to search for files.
        :param glob: A pattern which will be matched against files in the dataset.
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :return: The number of matching files
        """
        list_result = self.list_files(dataset_id, glob, is_dir)
        return len(list_result)

    def get_dataset_files(self, dataset_id, glob=".", version_number=None):
        """
        Retrieves URLs for the files matched by a glob or a path to a directory
        in a given dataset.

        :param dataset_id: The id of the dataset to retrieve files from
        :param glob: A regex used to select one or more files in the dataset
        :param version_number: The version number of the dataset to retrieve files from
        :return: A list of :class:`DatasetFile` objects matching the provided pattern.
        """
        if version_number is None:
            latest = True
        else:
            latest = False

        data = {
            "download_request": {
                "glob": glob,
                "isDir": is_dir,
                "latest": latest
            }
        }

        response = self._post_json(routes.matched_files(dataset_id), data)
        failure_message = "Failed to get matched files in dataset {}".format(dataset_id)
        versions = http_utils.get_success_json(response, failure_message)['versions']

        if version_number is None:
            version = versions[0]
        else:
            version = list(filter(lambda v: v['number'] == version_number, versions))

        return list(
            map(
                lambda f: DatasetFile(path=f['filename'], url=f['url']), version['files']
                )
            )

    def get_dataset_file(self, dataset_id, file_path, version = None):
        """
        Retrieves a dataset file matching a provided file path

        :param data_set_id: The id of the dataset to retrieve file from
        :param file_path: The file path within the dataset
        :param version: The dataset version to look for the file in. If nothing is supplied, the latest dataset version will be searched
        :return: A :class:`DatasetFile` object matching the filepath provided
        """
        if version == None:
            result = self._get(routes.file_dataset_path(dataset_id, file_path))
        else:
            result = self._get(routes.file_dataset_version_path(dataset_id, version, file_path))

        file = http_utils.get_success_json(result, "An error occurred retrieving file {}".format(file_path))['file']

        return DatasetFile(path=file['filename'], url=file['url'])

    def get_pif(self, dataset_id, uid, version = None):
        """
        Retrieves JSON representation of a PIF from a given dataset.

        :param data_set_id: The id of the dataset to retrieve PIF from
        :param uid: The uid of the PIF to retrieve
        :param version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :return: A :class:`Pif` object
        """
        if version == None:
            response = self._get(routes.pif_dataset_uid(dataset_id, uid))
        else:
            response = self._get(routes.pif_dataset_version_uid(dataset_id, uid, version))

        response = http_utils.check_success(response, "An error occurred retrieving PIF {}".format(uid))
        return pif.loads(response.content)

    def create_dataset(self, name=None, description=None, public=False):
        """
        Create a new data set.
        :param name: name of the dataset
        :param description: description for the dataset
        :param public: A boolean indicating whether or not the dataset should be public.

        :return: A :class:`Dataset` object representing the newly created dataset.
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
        response_dict = http_utils.get_success_json(result, failure_message)

        return _dataset_from_response_dict(response_dict)

    def update_dataset(self, dataset_id, name=None, description=None, public=None):
        """
        Update a data set.
        :param dataset_id:
        :param name: name of the dataset
        :param description: description for the dataset
        :param public: A boolean indicating whether or not the dataset should be public.
        :return: A :class:`Dataset` object representing the updated dataset.
        """
        data = {
            "public": _convert_bool_to_public_value(public)
        }

        if name:
            data["name"] = name
        if description:
            data["description"] = description

        dataset = {"dataset": data}

        response = http_utils.get_success_json(
                self._post_json(routes.update_dataset(dataset_id), data=dataset),
                "Failed to update dataset {}".format(dataset_id)
            )

        return _dataset_from_response_dict(response)

    def create_dataset_version(self, dataset_id):
        """
        Create a new data set version.

        :param dataset_id: The ID of the dataset for which the version must be bumped.
        :return: The number of the new version.
        """
        return http_utils.get_success_json(
                self._post_json(routes.create_dataset_version(dataset_id), data={}),
                "Failed to create dataset version for dataset {}".format(dataset_id)
            )['dataset_scoped_id']

def _dataset_from_response_dict(dataset):
    return Dataset(dataset['id'], name=dataset['name'],
        description=dataset['description'], created_at=dataset['created_at'])

def _convert_bool_to_public_value(val):
    if val == None:
        return None
    if val == False:
        return '0'
    if val == True:
        return '1'

def _get_s3_presigned_url(response_dict):
    """
    Helper method to create an S3 presigned url from the response dictionary.
    """
    url = response_dict['url']
    return url['scheme']+'://'+url['host']+url['path']+'?'+url['query']