def data_analysis(view_id):
  return 'data_views/{}/data_analysis'.format(view_id)

def data_view_predict(view_id):
    return 'data_views/{}/predict'.format(view_id)

def custom_model_predict(model_path):
    return 'ml_templates/{}/predict'.format(model_path)
