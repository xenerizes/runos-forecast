import numpy as np
from ml_metrics import ae


def ape(actual, predicted):
    return ae(actual, predicted) / actual


def mape(actual, predicted):
    return 100 * np.mean(ape(actual, predicted))
