from ..base import Model
from functools import reduce
import numpy as np


def _compute_ts(storage):
    ts = reduce(lambda x, y: x + y, storage.switch_load().values())
    const_load = map(lambda x: x.min(), storage.const_load().values())
    return ts + np.min(const_load)


class LoadModel(Model):
    def __init__(self, storage, components):
        Model.__init__(self, storage.load())
        self.components = components
        self.storage = storage

    def auto(self, order=None):
        self.model = _compute_ts(self. storage)
