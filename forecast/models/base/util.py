import numpy as np
from ml_metrics import ae


def ape(actual, predicted):
    maxes = [max(actual[i], predicted[i]) for i in range(len(predicted))]
    return np.abs(ae(actual, predicted) / maxes)


def mape(actual, predicted):
    return 100 * np.mean(ape(actual, predicted))
