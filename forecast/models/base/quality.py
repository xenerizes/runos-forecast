import ml_metrics


class ForecastQuality(object):
    def __init__(self, actual, fit):
        self._actual = actual
        self._fit = fit

    def mae(self):
        return ml_metrics.mae(self._actual, self._fit)

    def rmse(self):
        return ml_metrics.rmse(self._actual, self._fit)

    def ae(self):
        return ml_metrics.ae(self._actual, self._fit)

    def mse(self):
        return ml_metrics.mse(self._actual, self._fit)

    def se(self):
        return ml_metrics.se(self._actual, self._fit)

    def summary(self):
        res = {
            'Absolute Error': self.ae(),
            'Squared Error': self.se(),
            'Mean Absolute Error': self.ae(),
            'Mean Squared Error': self.mse(),
            'Root Mean Squared Error': self.rmse()
        }

        print("{:<15} {:<10}".format('Error', 'Score'))
        for k, v in res.items():
            print("{:<15} {:<10}".format(k, v))
