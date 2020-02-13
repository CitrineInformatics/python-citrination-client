descriptor_keys = [
    'formula',
    'Property Band gap',
    'Property Color',
    'Temperature (Property Band gap)',
    'Temperature (Property Color)'
]
data_view_config['descriptors'] = list(
    filter(
        lambda d: d['descriptor_key'] in descriptor_keys,
        data_view_config['descriptors']
    )
)
data_view_config['roles'] = {
    key: data_view_config['roles'][key] for key in descriptor_keys
}
