from citrination_client.base.errors import CitrinationClientError

class Target(object):
    """
    The optimization target for a design run. Consists of
    the name of the output column to optimize and the objective
    (either "Max" or "Min")
    """

    def __init__(self, name, objective):
        """
        Constructor.

        :param name: The name of the target output column
        :type name: str
        :param objective: The optimization objective; either "Min"
            or "Max"
        :type objective: str
        """
        if objective not in ["Max", "Min"]:
            raise CitrinationClientError(
                    "Target objective must either be \"Min\" or \"Max\""
                )

        self._name = name
        self._objective = objective

    def to_dict(self):
        return {
            "descriptor": self._name,
            "objective": self._objective
        }