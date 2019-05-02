# ... client initialization left out

linear_design = models_client.submit_design_run(data_view_id=data_view_id, num_candidates=10,
                                                effort=3,
                                                target=Target('Property Bulk modulus', .1), constraints=[],
                                                sampler='Default')
# Wait for the design to finish
print ("DesignUUID: " + linear_design.uuid)
while True:
    design_status = models_client.get_design_run_status(data_view_id, linear_design.uuid)
    if design_status.status == 'Finished':
        break
    time.sleep(5)

results = models_client.get_design_run_results(data_view_id, linear_design.uuid)
print(results.best_materials)
# [{'descriptor_values': {'formula': 'Ba', 'Property Bulk modulus': '9.0', ...