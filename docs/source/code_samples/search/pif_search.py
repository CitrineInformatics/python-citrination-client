# ... client initialization left out

search_client = client.search

# Construct a query which returns records in dataset 1160
# and have chemical formulas matching CoSi
query = PifSystemReturningQuery(
            query=DataQuery(
                dataset=DatasetQuery(
                    id=Filter(equal='1160')
                ),
                system=PifSystemQuery(
                    chemical_formula=ChemicalFieldQuery(
                        filter=ChemicalFilter(
                            equal='CoSi')))))

# Execute the search (we use pif_search because we have a PifSystemReturningQuery)
results = search_client.pif_search(query)

# Get the ID of the first hit
record_id = results.hits[0].id