from .base import BaseAlgorithm
from ..models.arima import ARIMAModel


class SimpleAlgorithm(BaseAlgorithm):
    def __init__(self, data, interval, history_len):
        BaseAlgorithm.__init__(self, data, interval, history_len)

    def select_model(self):
        self.model = ARIMAModel(self.history)

    def fit_model(self):
        self.model.auto()

    def next(self):
        if self.data.size - self.interval < self.end:
            self.start, self.end = 0, 0
        else:
            self.start, self.end = self.start + self.interval, self.end + self.interval
