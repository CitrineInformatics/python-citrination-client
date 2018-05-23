# ... client initialization left out

models_client = client.models

data_view_id = "4106"

resp = models_client.tsne(data_view_id)

band_gap_projection = resp.get_projection('Property Band gap')
band_gap_projection.xs # returns the x component of the TSNE projection
band_gap_projection.ys # returns the y component of the TSNE projection
band_gap_projection.responses # returns the responses for the points in the projection
band_gap_projection.uids # returns the record UIDs for the projection
band_gap_projection.tags # returns the tags on the points in the projection