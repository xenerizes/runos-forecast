import pandas as pd
import numpy as np
import ml_metrics


class Model(object):
    def __init__(self, ts):
        self._ts = pd.Series(ts.values, index=ts.index, dtype=np.float64)
        self._period = None
        self._model = None

    def append(self, date, value):
        pass

    def drop(self):
        self._ts = pd.Series()

    def get_fitted_values(self):
        return self._model.fittedvalues

    def auto(self, order=None):
        pass

    def predict(self, length):
        pass

    def min(self):
        return self._ts.min()

    def max(self):
        return self._ts.max()

    def mae(self):
        fitted = self.get_fitted_values()
        return ml_metrics.mae(self._ts, fitted)

    def rmse(self):
        fitted = self.get_fitted_values()
        return ml_metrics.rmse(self._ts, fitted)
