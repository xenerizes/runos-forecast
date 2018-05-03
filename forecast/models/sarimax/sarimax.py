from statsmodels.tsa.statespace.sarimax import SARIMAX

from ..base import Model
from ..arima import ARIMAModel


class SARIMAXModel(Model):
    def __init__(self, ts):
        Model.__init__(self, ts)
        self._order = None
        self._resid = None
        self._seasonal_order = None

    def select_order(self):
        arima = ARIMAModel(self._ts)
        arima.auto()
        self._resid = arima._model.resid
        return arima.select_order()

    def select_seasonal_order(self):
        arima_resid = ARIMAModel(self._resid)
        return arima_resid.select_order()

    def auto(self, order=None, seasonal_order=None, start_params=None):
        self._period = self._ts.index[1] - self._ts.index[0]
        self._order = order if order is not None else self.select_order()
        self._seasonal_order = seasonal_order if seasonal_order is not None else self.select_seasonal_order()
        self._model = SARIMAX(self._ts, order=self._order,
                              seasonal_order=self._seasonal_order,
                              enforce_stationarity=False,
                              enforce_invertibility=False).fit(start_params)

    def predict(self, length):
        start_date = self._model.fittedvalues.index[-1]
        end_date = start_date + length * self._period
        forecast = self._model.predict(start_date.isoformat(), end_date.isoformat())
        return forecast
