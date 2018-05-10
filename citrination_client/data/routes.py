from citrination_client.util.quote_finder import quote

def update_file(file_id):
    return 'data_sets/update_file/{}'.format(file_id)

def list_files(dataset_id):
    return 'datasets/{}/list_filepaths'.format(dataset_id)

def matched_files(dataset_id):
    return 'datasets/{}/download_files'.format(dataset_id)

def pif_dataset_uid(dataset_id, pif_uid):
    return 'datasets/{}/pif/{}'.format(dataset_id, pif_uid)

def pif_dataset_version_uid(dataset_id, version, pif_uid):
    return 'datasets/{}/version/{}/pif/{}'.format(dataset_id, version, pif_uid)

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