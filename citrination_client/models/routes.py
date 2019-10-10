def data_analysis(view_id):
  return 'data_views/{}/data_analysis'.format(view_id)

def submit_data_view_design(data_view_id):
    return "data_views/{}/experimental_design".format(data_view_id)

def get_data_view_design_status(data_view_id, run_uuid):
    return "data_views/{}/experimental_design/{}/status".format(data_view_id, run_uuid)

def get_data_view_design_results(data_view_id, run_uuid):
    return "data_views/{}/experimental_design/{}/results".format(data_view_id, run_uuid)

def kill_data_view_design_run(data_view_id, run_uuid):
    return "data_views/{}/experimental_design/{}".format(data_view_id, run_uuid)

def get_data_view_status(data_view_id):
    """
    URL for retrieving the statuses of all services
    associated with a data view.

    :param data_view_id: The ID of the desired data views
    :type data_view_id: str
    """
    return "data_views/{}/status".format(data_view_id)
