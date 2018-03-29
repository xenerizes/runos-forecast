from pandas.tseries.offsets import Second
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import arma_order_select_ic

from ..base.model import Model
from .util import is_stationary


class ARIMAModel(Model):
    def __init__(self, ts):
        Model.__init__(self, ts)
        self._order = None

    def select_order_brute_force(self):
        def objfunc(order, endog, exog):
            from statsmodels.tsa.arima_model import ARIMA
            fit = ARIMA(endog, order, exog).fit(full_output=False)
            return fit.aic

        ts = self.get_series()
        bic = arma_order_select_ic(ts).bic_min_order
        grid = (slice(bic[0], bic[0] + 1, 1), slice(1, 2, 1), slice(bic[1], bic[1] + 1, 1))
        from scipy.optimize import brute
        return brute(objfunc, grid, args=(ts, None), finish=None)

    def select_order(self):
        ts = self.get_series()
        if is_stationary(ts):
            bic = arma_order_select_ic(ts).bic_min_order
            return bic[0], 0, bic[1]

        ts1diff = ts.diff(periods=1).dropna()
        if is_stationary(ts1diff):
            bic = arma_order_select_ic(ts1diff).bic_min_order
            return bic[0], 1, bic[1]

        ts2diff = ts.diff(periods=2).dropna()
        bic = arma_order_select_ic(ts2diff).bic_min_order

        return bic[0], 2, bic[1]

    def get_fitted_values(self):
        return self._model.fittedvalues

    def auto(self):
        ts = self.get_series()
        self._period = ts.index[1] - ts.index[0]
        freq = Second(self._period.total_seconds())
        self._order = self.select_order()
        self._model = ARIMA(self.get_series(), order=self._order, freq=freq).fit()

    def predict(self):
        start_date = self._model.fittedvalues.index[-1]
        end_date = start_date + self._predict * self._period
        forecast = self._model.predict(start_date.isoformat(), end_date.isoformat())

        if self._order[1] > 0:
            shift = self.max() - self.min()
            forecast += shift

        return forecast

