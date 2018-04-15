from citrination_client.design.constraints.base import BaseConstraint

class CategoricalConstraint(BaseConstraint):

    def __init__(self, descriptor, categories):
        self._type = "categorical"
        self._descriptor = descriptor
        self._categories = categories

    def options(self):
        return {
            "categories": self._categories,
        }