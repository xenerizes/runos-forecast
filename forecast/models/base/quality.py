from ml_metrics import mse
from pandas import Series
from .util import mape, ape


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self.actual = actual
        self.fit = fit
        self.mse = '{:.1f}'.format(mse(self.actual, self.fit))
        self.mape = '{:.3f}%'.format(mape(self.actual, self.fit))

    def summary(self):
        data = [self.mse, self.mape]
        index = ['Mean Squared Error', 'Mean Absolute Percentage Error']
        return Series(data, index=index)

    def ape_series(self):
        return ape(self.actual, self.fit)
