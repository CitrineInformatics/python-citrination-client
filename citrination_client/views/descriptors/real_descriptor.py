from citrination_client.views.descriptors.descriptor import MaterialDescriptor


class RealDescriptor(MaterialDescriptor):
    def __init__(self, key, lower_bound, upper_bound, units=""):
        self.options = dict(lower_bound=lower_bound, upper_bound=upper_bound, units=units)
        super(RealDescriptor, self).__init__(key, "Real")

    def validate(self):
        raw_lower = self.options["lower_bound"]
        raw_upper = self.options["upper_bound"]

        try:
            lower = float(str(raw_lower))
            upper = float(str(raw_upper))
        except ValueError:
            raise ValueError(
                "lower_bound and upper_bound must be floats but got {} and {} respectively".format(
                    raw_lower, raw_upper)
            )

        if lower > upper:
            raise ValueError("Lower ({}) must be smaller than upper ({})".format(lower, upper))
