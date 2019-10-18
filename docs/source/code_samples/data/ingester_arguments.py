# ... client initialization left out
data_client = client.data

ingester_list = data_client.list_ingesters()
csv_ingester = ingester_list.find_by_id("citrine/ingest template_csv_converter")
formulation_ingester = ingester_list.find_by_id("citrine/ingest formulation_csv_converter")
xrdml_ingester = ingester_list.find_by_id("citrine/ingest xrdml_xrd_converter")

# Here we can see that the Template CSV ingester accepts no arguments
print(csv_ingester.arguments)
# []

# Here we can see that the Formulation CSV ingester accepts one optional argument
print(formulation_ingester.arguments)
# [{ 'name': 'check_ingredient_names',
#    'desc': 'Whether to check that the names of the ingredients in the formulations are present in this upload',
#    'type': 'Boolean',
#    'required': False }]

# Here we can see that the Citrine: XRD .xrdml ingester requires 2 arguments,
# one named `sample_id` and the other named `chemical_formula`, both of which
# should be strings.
print(xrdml_ingester.arguments)
# [{ 'name': 'sample_id',
#    'desc': 'An ID to uniquely identify the material referenced in the file.',
#    'type': 'String',
#    'required': True },
#  { 'name': 'chemical_formula',
#    'desc': 'The chemical formula of the material referenced in the file.',
#    'type': 'String',
#    'required': True }]
