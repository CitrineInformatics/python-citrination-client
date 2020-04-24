client = CitrinationClient(environ["CITRINATION_API_KEY"])

builder = DataViewBuilder()
builder.dataset_ids([187195])
    
formulation_desc = FormulationDescriptor("Formulation (idealMassPercent)")
builder.add_formulation_descriptor(formulation_desc, client.data_views)
