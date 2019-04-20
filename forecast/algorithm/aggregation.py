from .base import BaseAlgorithm
from ..models.load import LoadModel


class AggregationAlgorithm(BaseAlgorithm):
    def __init__(self, storage, components, opts):
        BaseAlgorithm.__init__(self, LoadModel, storage.load(), opts)
        self.model = LoadModel(storage, components)

    def step(self):
        pass
    
    def run(self):
        self.forecast = self.predict(0)
