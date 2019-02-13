from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class FormulationDescriptor(MaterialDescriptor):
    def __init__(self, key):
        self.options = dict()
        super(FormulationDescriptor, self).__init__(key, "Formulation")


