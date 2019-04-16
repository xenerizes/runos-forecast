from ..base import BaseAlgorithm
from .model_quality import ModelQuality


class CorrectiveAlgorithm(BaseAlgorithm):
    def __init__(self, model_class, data, opts):
        BaseAlgorithm.__init__(self, model_class, data, opts)
        self.quality = ModelQuality(opts.k)

    def needs_selection(self):
        return self.quality.is_bad()

    def select_model(self):
        self.model = self.model_class(self.history)

    def fit_model(self):
        self.model.auto()

    def next(self):
        if self.data.size - self.interval < self.end:
            self.start, self.end = 0, 0
        else:
            interval = self.interval + 1
            self.start, self.end = self.start + interval, self.end + interval
