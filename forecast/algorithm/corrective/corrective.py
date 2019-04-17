from pandas import Series
from pandas import DataFrame
from pandas import concat

from ..base import BaseAlgorithm
from .model_quality import ModelQuality


class CorrectiveAlgorithm(BaseAlgorithm):
    def __init__(self, model_class, data, opts):
        BaseAlgorithm.__init__(self, model_class, data, opts)
        self.quality = ModelQuality(opts.k)
        self.correction_interval = opts.corr_interval
        self.temp_forecast = Series()
        self.prev_forecast = None
        self.step_interval = self.interval - self.correction_interval + 1

    def needs_selection(self):
        if self.prev_forecast is None:
            return True

        prev_observed = self.data.iloc[self.end - self.step_interval:self.end]
        self.quality.append(prev_observed, self.prev_forecast)
        return self.quality.is_bad()

    def select_model(self):
        self.model = self.model_class(self.history)
        self.quality.clear()

    def fit_model(self):
        self.model.auto()

    def step(self):
        predicted = self.predict(self.interval)
        if self.temp_forecast.empty:
            self.temp_forecast = predicted
            return

        final_values = self.temp_forecast[self.correction_interval:]
        new_values = predicted[-self.correction_interval:]
        predicted = predicted[:-self.correction_interval]

        self.temp_forecast = predicted
        self.temp_forecast = self.temp_forecast.append(new_values)
        self.forecast = self.forecast.append(final_values)
        self.prev_forecast = final_values

    def next(self):
        if self.data.size - self.step_interval < self.end:
            self.start, self.end = 0, 0
        else:
            self.start, self.end = self.start + self.step_interval, self.end + self.step_interval
