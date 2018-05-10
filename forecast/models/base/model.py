import pandas as pd
import numpy as np


class Model(object):
    def __init__(self, ts):
        self.ts = pd.Series(ts.values, index=ts.index, dtype=np.float64)
        self.period = None
        self.model = None

    def append(self, date, value):
        pass

    def drop(self):
        self.ts = pd.Series()

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
