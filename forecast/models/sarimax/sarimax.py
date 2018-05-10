from statsmodels.tsa.statespace.sarimax import SARIMAX

from ..base import Model
from ..arima import ARIMAModel


class SARIMAXModel(Model):
    def __init__(self, ts):
        Model.__init__(self, ts)
        self.order = None
        self.resid = None
        self.seasonal_order = None

    def select_order(self):
        arima = ARIMAModel(self.ts)
        arima.auto()
        self.resid = arima.model.resid
        return arima.select_order()

    def select_seasonal_order(self):
        arima_resid = ARIMAModel(self.resid)
        return arima_resid.select_order()

    def auto(self, order=None, seasonal_order=None, start_params=None):
        self.period = self.ts.index[1] - self.ts.index[0]
        self.order = order if order is not None else self.select_order()
        self.seasonal_order = seasonal_order if seasonal_order is not None else self.select_seasonal_order()
        self.model = SARIMAX(self.ts, order=self.order,
                             seasonal_order=self.seasonal_order,
                             enforce_stationarity=False,
                             enforce_invertibility=False).fit(start_params)

    def predict(self, length):
        start_date = self.model.fittedvalues.index[-1]
        end_date = start_date + length * self.period
        forecast = self.model.predict(start_date.isoformat(), end_date.isoformat())
        return forecast
