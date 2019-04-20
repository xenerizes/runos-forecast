from ..base import BaseAlgorithm
from .model_quality import ModelQuality


class CorrectiveAlgorithm(BaseAlgorithm):
    def __init__(self, model_class, data, opts):
        BaseAlgorithm.__init__(self, model_class, data, opts)
        self.quality = ModelQuality(opts.k)
        self.correction_interval = opts.corr_interval
        self.prev_forecast = None
        self.step_interval = self.interval - self.correction_interval + 1

    def needs_selection(self):
        if self.prev_forecast is None:
            return True

        prev_observed = self.data.loc[self.prev_forecast.index]
        self.quality.append(prev_observed, self.prev_forecast)
        return self.quality.is_bad()

    def select_model(self):
        self.quality.clear()

    def fit_model(self, order=None):
        self.model = self.model_class(self.history)
        self.model.auto(order)

    def step(self):
        predicted = self.predict(self.interval)
        if self.correction_interval > 0:
            self.forecast.drop(self.forecast.index[-self.correction_interval:], inplace=True)
        self.forecast = self.forecast.append(predicted)
        self.prev_forecast = predicted

    def next(self):
        if self.data.size - self.step_interval < self.end:
            self.start, self.end = 0, 0
        else:
            self.start, self.end = self.start + self.step_interval, self.end + self.step_interval
