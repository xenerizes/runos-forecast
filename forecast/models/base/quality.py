import ml_metrics


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self.actual = actual
        self.fit = fit
        self.mae = ml_metrics.mae(self.actual, self.fit)
        self.rmse = ml_metrics.rmse(self.actual, self.fit)
        self.mse = ml_metrics.mse(self.actual, self.fit)

    def summary(self):
        return {
            'Mean Absolute Error': self.mae,
            'Mean Squared Error': self.mse,
            'Root Mean Squared Error': self.rmse
        }
