from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import arma_order_select_ic
import logging

from ..base.model import Model
from .util import is_stationary


def _arma_order_selector(ts, ic='bic'):
    res = arma_order_select_ic(ts, ic=ic, fit_kw={'method': 'css'})
    return getattr(res, '{}_min_order'.format(ic))


class ARIMAModel(Model):
    def __init__(self, ts):
        Model.__init__(self, ts)
        self.order = None

    def select_order_brute_force(self):
        def objfunc(order, endog, exog):
            from statsmodels.tsa.arima_model import ARIMA
            fit = ARIMA(endog, order, exog).fit(full_output=False)
            return fit.aic

        bic = arma_order_select_ic(self.ts, max_ar=6, max_ma=4).bic_min_order
        grid = (slice(bic[0], bic[0] + 1, 1), slice(1, 2, 1), slice(bic[1], bic[1] + 1, 1))
        from scipy.optimize import brute
        return brute(objfunc, grid, args=(self.ts, None), finish=None)

    def _select_order_impl(self, ic):
        if is_stationary(self.ts):
            bic = _arma_order_selector(self.ts, ic)
            return bic[0], 0, bic[1]

        ts1diff = self.ts.diff(periods=1).dropna()
        if is_stationary(ts1diff):
            bic = _arma_order_selector(ts1diff, ic)
            return bic[0], 1, bic[1]

        ts2diff = self.ts.diff(periods=2).dropna()
        bic = _arma_order_selector(ts2diff, ic)

        return bic[0], 2, bic[1]

    def select_order(self):
        return self._select_order_impl('bic')

    def reselect_order(self):
        return self._select_order_impl('aic')

    def auto(self, order=None):
        self.period = self.ts.index[1] - self.ts.index[0]
        self.order = order if order is not None else self.select_order()
        logging.debug('Model order is {}'.format(self.order))
        self.model = ARIMA(self.ts, order=self.order).fit(disp=False, method='css')

    def predict(self, length):
        start_date = self.model.fittedvalues.index[-1]
        end_date = start_date + length * self.period
        forecast = self.model.predict(start_date.isoformat(), end_date.isoformat())

        if self.order[1] > 0:
            shift = abs(self.model.fittedvalues[-1] - self.ts[-1])
            forecast += shift

        return forecast
