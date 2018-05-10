# ... client initialization left out

search_client = client.search

# Construct a query which returns records in dataset 1160
# which have GaN as a chemical formula and have band gap
# property values between 1.5 and 1.6
query = search_client.generate_simple_chemical_query(chemical_formula="GaN",
                                                     property_name="Band gap",
                                                     property_min=1.5,
                                                     property_max=1.6)

results = search_client.pif_search(query)

# Get the ID of the first hit
record_id = results.hits[0].id
print(results.hits[0].extracted)
# => {
#   u'property_units': u'eV',
#   u'property_value': u'1.57',
#   u'chemical_formula': u'GaN',
#   u'property_name': u'Band gap',
#   u'reference_doi': u'10.1038/s41524-017-0013-3'
# }