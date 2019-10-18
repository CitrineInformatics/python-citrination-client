# ... client initialization left out
data_client = client.data

# All ingesters available on your Citrination deployment
ingester_list = data_client.list_ingesters()
# Find all ingesters whose `name` attributes contain the phrase "xrd"
# Note that the `where` method returns a new IngesterList
xrd_ingesters = ingester_list.where({ "name": "xrd" })

# How many ingesters had names that contained "xrd"?
print(xrd_ingesters.ingester_count)
# 2

# Quick summary of what those ingesters are
print(xrd_ingesters)
# <IngesterList ingester_count=2 ingesters=[
#   "<Ingester id='citrine/ingest bruker_xrd_xy_prod'
#              display_name='Citrine: Bruker XRD .XY'
#              description='Converts Bruker V8 .XY files to PIF .json format.'
#              num_arguments='3'>",
#   "<Ingester id='citrine/ingest xrdml_xrd_converter'
#              display_name='Citrine: XRD .xrdml'
#              description='Converter for .xrdml files from XRD measurements'
#              num_arguments='2'>"
# ]>

# Supposing we want to go with the one whose display_name is `Citrine: XRD .xrdml`,
# there are several ways to do this:
# 1. Indexing into the xrd_ingesters' `ingesters` list:
xrdml_ingester = xrd_ingesters.ingesters[1]

# 2. Alternatively, using a where clause with the matching `display_name`, `id`,
#    or other searchable attribute:
xrdml_ingester = xrd_ingesters.where({ "display_name": "Citrine: XRD .xrdml" }).ingesters[0]

# 3. Since xrd_ingesters is an `IngesterList`, we could also use `find_by_id` to
#    avoid having to index into the `ingesters` list:
xrdml_ingester = xrd_ingesters.find_by_id("citrine/ingest xrdml_xrd_converter")
