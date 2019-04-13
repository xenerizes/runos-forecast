from ml_metrics import mse, ae
from pandas import Series
import numpy as np


def mape(actual, predicted):
    return np.mean(ae(actual, predicted)/actual)


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self.actual = actual
        self.fit = fit
        self.mse = mse(self.actual, self.fit)
        self.mape = mape(self.actual, self.fit)

    def summary(self):
        data = [self.mse, self.mape]
        index = ['Mean Squared Error', 'Mean Absolute Percentage Error']
        return Series(data, index=index)
