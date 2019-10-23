from citrination_client.util.quote_finder import quote

def update_file(file_id):
    return 'data_sets/update_file/{}'.format(file_id)

def list_files(dataset_id):
    return 'datasets/{}/list_filepaths'.format(dataset_id)

def matched_files(dataset_id):
    return 'datasets/{}/download_files'.format(dataset_id)

def pif_dataset_uid(dataset_id, pif_uid, pif_version = None, with_metadata = False):
    url = 'datasets/{}/pif/{}'.format(dataset_id, pif_uid)
    return _get_pif_url_helper(url, pif_version, with_metadata)

def pif_dataset_version_uid(dataset_id, version, pif_uid, pif_version = None, with_metadata = False):
    url = 'datasets/{}/version/{}/pif/{}'.format(dataset_id, version, pif_uid)
    return _get_pif_url_helper(url, pif_version, with_metadata)

def _get_pif_url_helper(url, pif_version, with_metadata):
    if pif_version:
        url += '/pif-version/{}'.format(pif_version)
    if with_metadata:
        url += '?with-metadata=true'
    return url

def create_dataset():
    return 'data_sets/create_dataset'

def create_dataset_version(dataset_id):
    return 'data_sets/{}/create_dataset_version'.format(dataset_id)

def update_dataset(dataset_id):
    return 'data_sets/{}/update'.format(dataset_id)

def upload_to_dataset(dataset_id):
    return 'data_sets/{}/upload'.format(dataset_id)

def file_dataset_path(dataset_id, file_path):
    return 'datasets/{}/file/{}'.format(dataset_id, quote(file_path))

def file_dataset_version_path(dataset_id, version, file_path):
    return 'datasets/{}/version/{}/files/{}'.format(dataset_id, version, quote(file_path))

def get_data_view_ids_path(dataset_id):
    return 'v1/datasets/{}/data-views'.format(dataset_id)
