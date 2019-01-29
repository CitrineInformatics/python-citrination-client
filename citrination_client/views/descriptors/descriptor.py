import json


class MaterialDescriptor(object):
    def __init__(self, key, category):
        self.key = key
        self.category = category

    def validate(self):
        pass

    def as_dict(self):
        self.validate()

        dict_repr = {
            "descriptor_key": self.key,
            "category": self.category
        }

        dict_repr.update(self.options)

        return dict_repr

    def __repr__(self):
        return json.dumps(self.as_dict(), indent=2)
