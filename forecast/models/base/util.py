import numpy as np
from ml_metrics import ae


def ape(actual, predicted):
    return np.abs(ae(actual.abs(), predicted.abs()) / actual.abs())


def mape(actual, predicted):
    return 100 * np.mean(ape(actual, predicted))
