import pandas as pd
import ml_metrics


class Model(object):
    def __init__(self, ts):
        self._ts = ts
        self._predict = 0
        self._period = None
        self._model = None

    def append(self, date, value):
        pass

    def drop(self):
        self._ts = pd.Series()

    def get_series(self):
        return self._ts

    def get_fitted_values(self):
        pass

    def auto(self):
        pass

    def predict(self):
        pass

    def min(self):
        return self._ts.min()

    def max(self):
        return self._ts.max()

    def mae(self):
        actual = self.get_series()
        fitted = self.get_fitted_values()
        return ml_metrics.mae(actual, fitted)

    def rmse(self):
        actual = self.get_series()
        fitted = self.get_fitted_values()
        return ml_metrics.rmse(actual, fitted)
