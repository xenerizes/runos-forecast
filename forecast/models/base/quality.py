import ml_metrics
import pandas as pd


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self.actual = actual
        self.fit = fit
        self.mae = ml_metrics.mae(self.actual, self.fit)
        self.rmse = ml_metrics.rmse(self.actual, self.fit)
        self.mse = ml_metrics.mse(self.actual, self.fit)

    def summary(self):
        data = [self.mae, self.mse, self.rmse]
        index = ['Mean Absolute Error', 'Mean Squared Error', 'Root Mean Squared Error']
        return pd.Series(data, index=index)
