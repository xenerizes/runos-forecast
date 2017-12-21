import pandas as pd
import ml_metrics


class Model(object):
    def __init__(self):
        self._dates = []
        self._values = []
        self._predict = 0
        self._period = None
        self._model = None

    def append(self, date, value):
        self._dates.append(date)
        self._values.append(value)

    def drop(self):
        self._dates = []
        self._values = []

    def get_series(self):
        return pd.Series(data=self._values, index=pd.to_datetime(self._dates))

    def get_fitted_values(self):
        pass

    def auto(self):
        pass

    def predict(self):
        pass

    def min(self):
        return min(self._values)

    def max(self):
        return max(self._values)

    def mae(self):
        actual = self.get_series()
        fitted = self.get_fitted_values()
        return ml_metrics.mae(actual, fitted)

    def rmse(self):
        actual = self.get_series()
        fitted = self.get_fitted_values()
        return ml_metrics.rmse(actual, fitted)
