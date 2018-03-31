import ml_metrics


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self._actual = actual
        self._fit = fit
        self.mae = ml_metrics.mae(self._actual, self._fit)
        self.rmse = ml_metrics.rmse(self._actual, self._fit)
        self.mse = ml_metrics.mse(self._actual, self._fit)

    def summary(self):
        return {
            'Mean Absolute Error': self.mae,
            'Mean Squared Error': self.mse,
            'Root Mean Squared Error': self.rmse
        }
