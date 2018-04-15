class BaseConstraint(object):

    def to_dict(self):
        return {
            "name": self._descriptor,
            "type": self._type,
            "options": self.options()
        }
