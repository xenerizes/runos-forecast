from .base import BaseAlgorithm
from ..models.sarimax import SARIMAXModel


class SimpleSeasonalAlgorithm(BaseAlgorithm):
    def __init__(self, data, interval, history_len):
        BaseAlgorithm.__init__(self, data, interval, history_len)

    def select_model(self):
        self.model = SARIMAXModel(self.history)

    def fit_model(self):
        self.model.auto()

    def next(self):
        if self.data.size - self.interval < self.end:
            self.start, self.end = 0, 0
        else:
            interval = self.interval + 1
            self.start, self.end = self.start + interval, self.end + interval
