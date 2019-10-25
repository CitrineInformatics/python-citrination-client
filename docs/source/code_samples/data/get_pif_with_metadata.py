# ... client initialization left out
data_client = client.data
dataset_id = 105924
pif_uid = "1DF1C8EB706363E40546253D5D025D90"

get_pif_with_metadata = data_client.get_pif_with_metadata(dataset_id, pif_uid)

print(get_pif_with_metadata)
# {'metadata': {
#     'uid': '1DF1C8EB706363E40546253D5D025D90',
#     'version': 1,
#     'dataset_id': '105924',
#     'dataset_version': 1,
#     'updated_at': '2017-07-04T19:41:40.139Z'},
#  'pif': <pypif.obj.system.chemical.chemical_system.ChemicalSystem at 0x1131b8a50>}
