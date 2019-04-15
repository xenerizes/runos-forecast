from statsmodels.tsa.statespace.sarimax import SARIMAX
from numpy import zeros

from ..base import Model
from ..arima import ARIMAModel


class SARIMAXModel(Model):
    def __init__(self, ts):
        Model.__init__(self, ts)
        self.order = None
        self.seasonal_order = None

    def select_order(self):
        arima = ARIMAModel(self.ts)
        arima.auto()
        return arima.select_order()

    def auto(self, order=None):
        self.period = self.ts.index[1] - self.ts.index[0]
        self.order = order if order is not None else self.select_order()
        print(self.order)
        p, d, q = self.order
        start_params_size = p + d + q + 1
        start_params = zeros(start_params_size)
        model_type = SARIMAX(self.ts, order=self.order)
        self.model = model_type.fit(start_params=start_params, disp=False)

    def predict(self, length):
        start_date = self.model.fittedvalues.index[-1]
        end_date = start_date + length * self.period
        forecast = self.model.predict(start_date.isoformat(), end_date.isoformat())
        return forecast
