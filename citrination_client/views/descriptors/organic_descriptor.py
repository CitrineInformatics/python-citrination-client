from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class OrganicDescriptor(MaterialDescriptor):
    def __init__(self, key):
        self.options = dict()
        super(OrganicDescriptor, self).__init__(key, "Organic")

