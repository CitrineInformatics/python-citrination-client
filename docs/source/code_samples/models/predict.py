# ... client initialization left out

models_client = client.models

# The input to this data view is a SMILES string
inputs = [
  {"formula": "NaCl", "Property Crystallinity": "Amorphous"},
  {"formula": "MgO2", "Property Crystallinity": "Polycrystalline"}
]

data_view_id = "4106"

# This prediction will return a list of two PredictionResult objects since
# there were two candidates passed in as inputs.
prediction_results = models_client.predict(data_view_id, inputs, method="scalar")

# Retrieve the prediction value and loss for the "Property Band gap" output
# for the NaCl candidate
nacl_result = prediction_results[0]
nacl_value = nacl_result.get_value("Property Band gap").value
nacl_loss = nacl_result.get_value("Property Band gap").loss