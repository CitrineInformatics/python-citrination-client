class DesignResults(object):

    def __init__(self, best_materials, next_experiments):
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