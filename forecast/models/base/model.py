from pandas import Series
from numpy import float64


class Model(object):
    def __init__(self, ts):
        self.ts = Series(ts.values, index=ts.index, dtype=float64)
        self.period = None
        self.model = None

    def append(self, date, value):
        pass

    def drop(self):
        self.ts = Series()

    def get_fitted_values(self):
        return self.model.fittedvalues

    def auto(self, order=None):
        pass

    def predict(self, length):
        pass

    def min(self):
        return self.ts.min()

    def max(self):
        return self.ts.max()
