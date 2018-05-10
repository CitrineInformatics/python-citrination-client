# ... client initialization left out

search_client = client.search

# Construct a query which returns datasets
# which contain records with chemical formulas
# matching MgO2
query = DatasetReturningQuery(
            query=DataQuery(
                system=PifSystemQuery(
                    chemical_formula=ChemicalFieldQuery(
                        filter=ChemicalFilter(
                            equal='MgO2')))))

# Execute the search; we use dataset_search because
# we have a DatasetReturningQuery
results = search_client.dataset_search(query)

# The resulting hits represent datasets which
# contain records that matched our criteria
print(results.hits[0].name)
# => Wikipedia

print(results.hits[0].id)
# => 114201