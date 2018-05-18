from ml_metrics import mae, rmse, mse
from pandas import Series


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self.actual = actual
        self.fit = fit
        self.mae = mae(self.actual, self.fit)
        self.rmse = rmse(self.actual, self.fit)
        self.mse = mse(self.actual, self.fit)

    def summary(self):
        data = [self.mae, self.mse, self.rmse]
        index = ['Mean Absolute Error', 'Mean Squared Error', 'Root Mean Squared Error']
        return Series(data, index=index)
