from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class InorganicDescriptor(MaterialDescriptor):
    def __init__(self, key, threshold):
        self.options = dict(threshold=threshold)
        super(InorganicDescriptor, self).__init__(key, "Inorganic")


