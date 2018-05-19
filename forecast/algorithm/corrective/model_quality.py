from ml_metrics import rmse, mae
from statsmodels.tsa.filters.hp_filter import hpfilter

from .metric import Metric
from .util import corr_dist

LAMB = 0.001


class ModelQuality(object):
    def __init__(self, k):
        metric_callable_list = [corr_dist, rmse, mae]
        self.metrics = [Metric(func, k) for func in metric_callable_list]

    def append(self, actual, predicted):
        actual_trend = hpfilter(actual, lamb=LAMB)
        predicted_trend = hpfilter(predicted, lamb=LAMB)
        for metric in self.metrics:
            metric.append(actual_trend, predicted_trend)

    def is_bad(self):
        bad_metrics = [1 for metric in self.metrics if metric.is_bad()]
        return sum(bad_metrics) > 0

    def clear(self):
        for metric in self.metrics:
            metric.clear()
