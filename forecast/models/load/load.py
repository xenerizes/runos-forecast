from ..base import Model
from functools import reduce


class LoadModel(Model):
    def __init__(self, storage, components):
        Model.__init__(self, storage.load())
        self.components = components
        self.storage = storage

    def predict(self, length):
        return self._compute_ts()

    def _compute_ts(self):
        ts = reduce(lambda x, y: x.add(y, fill_value=0), self.components)
        const_load = list(map(lambda x: x.min(), self.storage.const_load().values()))
        return ts + sum(const_load)
