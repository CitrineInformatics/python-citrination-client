from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class AlloyCompositionDescriptor(MaterialDescriptor):
    def __init__(self, key, balance_element, basis=100, threshold=None):
        self.options = dict(balance_element=balance_element, basis=basis, threshold=threshold)
        super(AlloyCompositionDescriptor, self).__init__(key, "Alloy composition")


