from pandas import DataFrame, MultiIndex
from .series import TimeSeries
from .util import cut
from forecast.models.base.quality import ForecastQuality

OVERLOAD_BOUNDS = [0.75, 0.8, 0.85, 0.9, 0.95]
INTERVALS = [2, 3, 5]


class ExecutionSummary(object):
    def __init__(self, actual, predicted):
        actual, predicted = cut(actual, predicted)
        self.actual, self.predicted = tuple(TimeSeries(data) for data in [actual, predicted])

    def quality(self):
        result = ForecastQuality(self.actual.data, self.predicted.data).summary()
        return result.to_frame("Value")

    def detection_summary(self):
        overloads = []
        fps = []
        totals = []
        index = []
        for size in OVERLOAD_BOUNDS:
            for interval in INTERVALS:
                detected, fp, total = self.overloads(size, interval)
                overloads.append(detected)
                fps.append(fp)
                totals.append(total)
                index.append((size, interval))

        data = {
            "TP": overloads,
            "FP": fps,
            "total": totals
        }
        index = MultiIndex.from_tuples(index, names=['size', 'interval'])

        return DataFrame(data, index=index)

    def overloads(self, size, interval):
        overloads = self.actual.overloads(size)
        predicted = self.predicted.overloads(size)
        detected = []
        for overload in overloads:
            observe = self.predicted.quality_interval(overload, interval)
            if len(observe.overloads(size)) > 0:
                detected.append(overload)

        tp_count = len(detected)
        fp_count = len(predicted) - len(detected)
        overload_count = len(overloads)

        if overload_count == 0:
            return 0, 0, 0

        tp_percentage, fp_percentage = tuple(100 * float(count) / overload_count for count in [tp_count, fp_count])
        return tp_percentage, fp_percentage, overload_count
