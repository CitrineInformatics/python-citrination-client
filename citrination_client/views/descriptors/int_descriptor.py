from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class IntDescriptor(MaterialDescriptor):
    def __init__(self, key, lower_bound, upper_bound, units=""):
        self.options = dict(lower_bound=lower_bound, upper_bound=upper_bound, units=units)
        super(IntDescriptor, self).__init__(key, "Integer")

    def validate(self):
        raw_lower = self.options["lower_bound"]
        raw_upper = self.options["upper_bound"]

        try:
            lower = int(str(raw_lower))
            upper = int(str(raw_upper))
        except ValueError:
            raise ValueError(
                "lower_bound and upper_bound must be integers but got {} and {} respectively".format(
                    raw_lower, raw_upper)
            )

        if lower > upper:
            raise ValueError("Lower ({}) must be smaller than upper ({})".format(lower, upper))
