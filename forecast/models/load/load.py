from ..base import Model
from functools import reduce


def _compute_ts(storage):
    ts = reduce(lambda x, y: x + y, storage.switch_load().values())
    const_load = map(lambda x: x.min(), storage.const_load().values())
    return ts + reduce(lambda x, y: x + y, const_load)


class LoadModel(Model):
    def __init__(self, storage, components):
        Model.__init__(self, storage.load())
        self.components = components
        self.storage = storage

    def predict(self, length):
        return _compute_ts(self.storage)
