from citrination_client.views.descriptors.descriptor import MaterialDescriptor
from citrination_client.base.errors import CitrinationClientError

from six import string_types


class CategoricalDescriptor(MaterialDescriptor):
    def __init__(self, key, categories=[]):
        self.options = dict(descriptor_values=categories)
        super(CategoricalDescriptor, self).__init__(key, "Categorical")

    def validate(self):
        categories = self.options['descriptor_values']
        if type(categories) is not list:
            raise CitrinationClientError("CategoricalColumn requires that the categories value is a list of strings")

        if not all(isinstance(item, string_types) for item in categories):
            raise CitrinationClientError("CategoricalColumn requires that the categories value is a list of strings")

