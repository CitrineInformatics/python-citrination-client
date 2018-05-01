# ... client initialization left out

models_client = citrination_client.models

# The input to this data view is a SMILES string
inputs = [
  {"SMILES": "c1(C=O)cc(OC)c(O)cc1"},
  {"SMILES": "C=C"}
]

data_view_id = "177"

# This prediction will return a list of two PredictionResult objects since
# there were two candidates passed in as inputs.
prediction_results = models_client.predict(data_view_id, inputs, method="scalar")