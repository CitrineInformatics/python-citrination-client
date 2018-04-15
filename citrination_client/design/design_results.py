class DesignResults(object):
    """
    The result of a design run. Consists of a set of dictionaries representing
    the candidates which are the best materials according to the target
    and the constraints and a set of dictionaries representing candidates
    which would be the most useful in improving the quality of the model.
    """

    def __init__(self, best_materials, next_experiments):
        """
        Constructor.

        :param best_materials: An array of candidate dictionaries
        :type best_materials: list of dictionaries
        :param next_experiments: An array of candidate dictionaries
        :type next_experiments: list of dictionaries
        """
        self._best_materials = best_materials
        self._next_experiments = next_experiments

    @property
    def best_materials(self):
        return self._best_materials

    @best_materials.setter
    def best_materials(self, value):
        self._best_materials = value

    @best_materials.deleter
    def best_materials(self):
        self._best_materials = None

    @property
    def next_experiments(self):
        return self._next_experiments

    @next_experiments.setter
    def next_experiments(self, value):
        self._next_experiments = value

    @next_experiments.deleter
    def next_experiments(self):
        self._next_experiments = None