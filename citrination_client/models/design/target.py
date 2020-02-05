from citrination_client.base.errors import CitrinationClientError


class Target(object):
    """
    The optimization target for a design run. Consists of
    the name of the output column to optimize and the objective
    (either "Max" or "Min", or a scalar value (such as "5.0"))
    """

    def __init__(self, name, objective):
        """
        Constructor.

        :param name: The name of the target output column
        :type name: str
        :param objective: The optimization objective; "Min", "Max", or a scalar value (such as "5.0")
        :type objective: str
        """

        try:
            self._objective = float(objective)
        except ValueError:
            if objective.lower() not in ["max", "min"]:
                raise CitrinationClientError(
                    "Target objective must either be \"min\" or \"max\""
                )
            self._objective = objective

        self._name = name

    def to_dict(self):
        return {
            "descriptor": self._name,
            "objective": self._objective
        }
