class BaseConstraint(object):

    def to_dict(self):
        """
        Returns a dictionary representing the constraint.
        Assists in JSON serialization.

        :return: A dictionary with the name and type of the constraint
            along with any type-specific metadata the constraint may
            require
        """
        return {
            "name": self._name,
            "type": self._type,
            "options": self.options()
        }
