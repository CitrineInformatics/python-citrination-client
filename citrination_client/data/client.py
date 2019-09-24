from citrination_client.base.base_client import BaseClient
from citrination_client.base.errors import *
from citrination_client.data import *
from citrination_client.data import routes as routes

from pypif import pif

import os
import shutil
import requests

class DataClient(BaseClient):
    """
    Client encapsulating data management behavior.
    """

    def __init__(self, api_key, host="https://citrination.com", suppress_warnings=False, proxies=None):
        """
        Constructor.

        :param api_key: A users API key, as a string
        :type api_key: str
        :param host: The base URL of the citrination site, e.g. https://citrination.com
        :type host: str
        :param suppress_warnings: Whether or not usage warnings should be
            printed to stdout
        :type suppress_warnings: bool
        """
        members = [
            "upload",
            "list_files",
            "matched_file_count",
            "get_dataset_files",
            "get_dataset_file",
            "download_files",
            "create_dataset",
            "create_dataset_version",
            "get_ingest_status",
            "get_pif",
            "update_dataset",
            "delete_dataset",
            "get_data_view_ids"
        ]
        super(DataClient, self).__init__(
            api_key, host, members, suppress_warnings, proxies
        )

    def upload(self, dataset_id, source_path, dest_path=None):
        """
        Upload a file, specifying source and dest paths a file (acts as the scp command).asdfasdf

        :param dataset_id: The ID of the dataset to search for files.
        :type dataset_id: Union[int, str]
        :param source_path: The path to the file on the source host asdf
        :type source_path: str
        :param dest_path: The path to the file where the contents of the upload will be written (on the dest host)
        :type dest_path: str
        :return: The result of the upload process
        :rtype: :class:`UploadResult`
        """
        upload_result = UploadResult()
        source_path = str(source_path)
        if not dest_path:
            dest_path = source_path
        else:
            dest_path = str(dest_path)

        if os.path.isdir(source_path):
            for path, subdirs, files in os.walk(source_path):
                relative_path = os.path.relpath(path, source_path)
                current_dest_prefix = dest_path
                if relative_path is not ".":
                    current_dest_prefix = os.path.join(
                        current_dest_prefix, relative_path
                    )
                for name in files:
                    current_dest_path = os.path.join(current_dest_prefix, name)
                    current_source_path = os.path.join(path, name)
                    try:
                        file_upload_result = self.upload(
                            dataset_id, current_source_path, current_dest_path
                        )
                        if file_upload_result.successful():
                            upload_result.add_success(current_source_path)
                        else:
                            upload_result.add_failure(
                                current_source_path, "Upload failure"
                            )
                    except (CitrinationClientError, ValueError) as e:
                        upload_result.add_failure(current_source_path, str(e))

            return upload_result

        elif os.path.isfile(source_path):
            path_data = {
                "dest_path": str(dest_path),
                "src_path": str(source_path)
            }
            file_data = self._get_success_json(
                self._post_json(
                    routes.upload_to_dataset(dataset_id), data = path_data
                )
            )
            s3url = _get_s3_presigned_url(file_data)

            with open(source_path, 'rb') as f:
                if os.stat(source_path).st_size == 0:
                    # Upload a null character as a placeholder for
                    # the empty file since Citrination does not support
                    # truly empty files
                    data = "\0"
                else:
                    data = f

                s3_response = requests.put(
                    s3url,
                    data = data,
                    headers = file_data["required_headers"],
                    proxies = self.proxies
                )
                if s3_response.status_code == 200:
                    data = {
                        's3object': file_data['url']['path'],
                        's3bucket': file_data['bucket']
                    }
                    self._post_json(
                        routes.update_file(file_data['file_id']), data = data
                    )
                    upload_result.add_success(source_path)
                    return upload_result
                else:
                    raise CitrinationClientError(
                        "Failure to upload {} to Citrination".format(source_path)
                    )

        else:
            raise ValueError("No file at specified path {}".format(source_path))

    def list_files(self, dataset_id, glob=".", is_dir=False):
        """
        List matched filenames in a dataset on Citrination.

        :param dataset_id: The ID of the dataset to search for files.
        :type dataset_id: int
        :param glob: A pattern which will be matched against files in the dataset.
        :type glob: str
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :type is_dir: bool
        :return: A list of filepaths in the dataset matching the provided glob.
        :rtype: list of strings
        """
        data = {
            "list": {
                "glob": glob,
                "isDir": is_dir
            }
        }
        return self._get_success_json(self._post_json(routes.list_files(dataset_id), data, failure_message="Failed to list files for dataset {}".format(dataset_id)))['files']

    def matched_file_count(self, dataset_id, glob=".", is_dir=False):
        """
        Returns the number of files matching a pattern in a dataset.

        :param dataset_id: The ID of the dataset to search for files.
        :type dataset_id: int
        :param glob: A pattern which will be matched against files in the dataset.
        :type glob: str
        :param is_dir: A boolean indicating whether or not the pattern should match against the beginning of paths in the dataset.
        :type is_dir: bool
        :return: The number of matching files
        :rtype: int
        """
        list_result = self.list_files(dataset_id, glob, is_dir)
        return len(list_result)

    def get_ingest_status(self, dataset_id):
        """
        Returns the current status of dataset ingestion.  If any file uploaded to a dataset is in an error/failure state
        this endpoint will return error/failure.  If any files are still processing, will return processing.

        :param dataset_id: Dataset identifier
        :return: Status of dataset ingestion as a string
        """
        failure_message = "Failed to create dataset ingest status for dataset {}".format(dataset_id)
        response = self._get_success_json(
            self._get('v1/datasets/' + str(dataset_id) + '/ingest-status',
                            failure_message=failure_message))['data']

        if 'status' in response:
            return response['status']
        return ''

    def get_dataset_files(self, dataset_id, glob=".", is_dir=False, version_number=None):
        """
        Retrieves URLs for the files matched by a glob or a path to a directory
        in a given dataset.

        :param dataset_id: The id of the dataset to retrieve files from
        :type dataset_id: int
        :param glob: A regex used to select one or more files in the dataset
        :type glob: str
        :param is_dir: Whether or not the supplied pattern should be treated as a directory to search in
        :type is_dir: bool
        :param version_number: The version number of the dataset to retrieve files from
        :type version_number: int
        :return: A list of dataset files whose paths match the provided pattern.
        :rtype: list of :class:`DatasetFile`
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

        failure_message = "Failed to get matched files in dataset {}".format(dataset_id)

        versions = self._get_success_json(self._post_json(routes.matched_files(dataset_id), data, failure_message=failure_message))['versions']

        # if you don't provide a version number, only the latest
        # will be included in the response body
        if version_number is None:
            version = versions[0]
        else:
            try:
                version = list(filter(lambda v: v['number'] == version_number, versions))[0]
            except IndexError:
                raise ResourceNotFoundException()

        return list(
            map(
                lambda f: DatasetFile(path=f['filename'], url=f['url']), version['files']
                )
            )

    def get_dataset_file(self, dataset_id, file_path, version = None):
        """
        Retrieves a dataset file matching a provided file path

        :param dataset_id: The id of the dataset to retrieve file from
        :type dataset_id: int
        :param file_path: The file path within the dataset
        :type file_path: str
        :param version: The dataset version to look for the file in. If nothing is supplied, the latest dataset version will be searched
        :type version: int
        :return: A dataset file matching the filepath provided
        :rtype: :class:`DatasetFile`
        """
        return self.get_dataset_files(dataset_id, "^{}$".format(file_path), version_number=version)[0]

    def download_files(self, dataset_files, destination='.'):
        """
        Downloads file(s) to a local destination.

        :param dataset_files:
        :type dataset_files: list of :class: `DatasetFile`
        :param destination: The path to the desired local download destination
        :type destination: str
        :param chunk: Whether or not to chunk the file. Default True
        :type chunk: bool
        """
        if not isinstance(dataset_files, list):
            dataset_files = [dataset_files]

        for f in dataset_files:
            filename = f.path.lstrip('/')
            local_path = os.path.join(destination, filename)

            if not os.path.isdir(os.path.dirname(local_path)):
                os.makedirs(os.path.dirname(local_path))

            r = requests.get(f.url, stream=True, proxies = self.proxies)

            with open(local_path, 'wb') as output_file:
                shutil.copyfileobj(r.raw, output_file)

    def get_pif(self, dataset_id, uid, dataset_version = None):
        """
        Retrieves a PIF from a given dataset.

        :param dataset_id: The id of the dataset to retrieve PIF from
        :type dataset_id: int
        :param uid: The uid of the PIF to retrieve
        :type uid: str
        :param dataset_version: The dataset version to look for the PIF in. If nothing is supplied, the latest dataset version will be searched
        :type dataset_version: int
        :return: A :class:`Pif` object
        :rtype: :class:`Pif`
        """
        failure_message = "An error occurred retrieving PIF {}".format(uid)
        if dataset_version == None:
            response = self._get(routes.pif_dataset_uid(dataset_id, uid), failure_message=failure_message)
        else:
            response = self._get(routes.pif_dataset_version_uid(dataset_id, dataset_version, uid), failure_message=failure_message)

        return pif.loads(response.content.decode("utf-8"))

    def create_dataset(self, name=None, description=None, public=False):
        """
        Create a new data set.

        :param name: name of the dataset
        :type name: str
        :param description: description for the dataset
        :type description: str
        :param public: A boolean indicating whether or not the dataset should be public.
        :type public: bool
        :return: The newly created dataset.
        :rtype: :class:`Dataset`
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
        result = self._get_success_json(self._post_json(routes.create_dataset(), dataset, failure_message=failure_message))

        return _dataset_from_response_dict(result)

    def update_dataset(self, dataset_id, name=None, description=None, public=None):
        """
        Update a data set.

        :param dataset_id: The ID of the dataset to update
        :type dataset_id: int
        :param name: name of the dataset
        :type name: str
        :param description: description for the dataset
        :type description: str
        :param public: A boolean indicating whether or not the dataset should
            be public.
        :type public: bool
        :return: The updated dataset.
        :rtype: :class:`Dataset`
        """
        data = {
            "public": _convert_bool_to_public_value(public)
        }

        if name:
            data["name"] = name
        if description:
            data["description"] = description

        dataset = {"dataset": data}
        failure_message = "Failed to update dataset {}".format(dataset_id)
        response = self._get_success_json(self._post_json(routes.update_dataset(dataset_id), data=dataset, failure_message=failure_message))

        return _dataset_from_response_dict(response)

    def delete_dataset(self, dataset_id):
        """
        Delete a dataset by id.  This will only work if you are the owner of the dataset.

        :param dataset_id: The ID of the dataset to data.
        """
        failure_message = "Dataset delete failed"
        self._delete('v1/datasets/' + str(dataset_id), None, failure_message=failure_message)

    def create_dataset_version(self, dataset_id):
        """
        Create a new data set version.

        :param dataset_id: The ID of the dataset for which the version must be bumped.
        :type dataset_id: int
        :return: The new dataset version.
        :rtype: :class:`DatasetVersion`
        """
        failure_message = "Failed to create dataset version for dataset {}".format(dataset_id)
        number = self._get_success_json(self._post_json(routes.create_dataset_version(dataset_id), data={}, failure_message=failure_message))['dataset_scoped_id']

        return DatasetVersion(number=number)

    def get_data_view_ids(self, dataset_id):
        """
        Returns a list of ids for data views that are built upon the provided dataset.

        :param dataset_id: The ID of the dataset for which the version must be bumped.
        :type dataset_id: int
        :return: The list of data view ids that use the given dataset.
        :rtype: list of int
        """
        failure_message = "Failed to get data view ids for dataset {}".format(dataset_id)
        return self._get_success_json(
            self._get(
                routes.get_data_view_ids_path(dataset_id), failure_message=failure_message
            )
        )['data']

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
    # for backwards compatability, support the old API #utahisrad
    if val == '0' or val == '1':
        return val

def _get_s3_presigned_url(response_dict):
    """
    Helper method to create an S3 presigned url from the response dictionary.
    """
    url = response_dict['url']
    return url['scheme']+'://'+url['host']+url['path']+'?'+url['query']
