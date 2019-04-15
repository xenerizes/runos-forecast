from .base import BaseAlgorithm
from ..models.load import LoadModel


class AggregationAlgorithm(BaseAlgorithm):
    def __init__(self, storage, components, history_len):
        BaseAlgorithm.__init__(self, LoadModel, storage.load(), 0, history_len)
        self.model = LoadModel(storage, components)

    def step(self):
        pass
    
    def run(self):
        self.forecast = self.predict(0)[self.history_len:]
