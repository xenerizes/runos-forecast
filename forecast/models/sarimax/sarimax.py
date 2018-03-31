from statsmodels.tsa.statespace.sarimax import SARIMAX

from ..arima import ARIMAModel


class SARIMAXModel(ARIMAModel):
    def auto(self, order=None, seasonal_order=None, start_params=None):
        self._period = self._ts.index[1] - self._ts.index[0]
        self._order = order if order is not None else self.select_order()
        self._model = SARIMAX(self._ts, order=self._order,
                              seasonal_order=seasonal_order,
                              enforce_stationarity=False,
                              enforce_invertibility=False).fit(start_params)
