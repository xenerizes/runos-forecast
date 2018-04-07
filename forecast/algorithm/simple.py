from .base import BaseAlgorithm
from ..models.arima import ARIMAModel


class SimpleAlgorithm(BaseAlgorithm):
    def __init__(self, storage, interval, history_len):
        BaseAlgorithm.__init__(self, storage, interval, history_len)

    def select_model(self):
        self._model = ARIMAModel(self._history)

    def fit_model(self):
        self._model.auto()
