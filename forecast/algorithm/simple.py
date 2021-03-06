from .base import BaseAlgorithm


class SimpleAlgorithm(BaseAlgorithm):
    def __init__(self, model_class, data, opts):
        BaseAlgorithm.__init__(self, model_class, data, opts)

    def select_model(self):
        self.model = self.model_class(self.history)
        return self.model.select_order()

    def fit_model(self, order=None):
        self.model.auto(order)

    def next(self):
        if self.data.size - self.interval < self.end:
            self.start, self.end = 0, 0
        else:
            interval = self.interval + 1
            self.start, self.end = self.start + interval, self.end + interval
