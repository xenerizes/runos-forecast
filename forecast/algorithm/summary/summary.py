from pandas import DataFrame, MultiIndex

from forecast.models.base.quality import ForecastQuality

from .series import TimeSeries
from .util import cut

OVERLOAD_BOUNDS = [0.8, 0.85, 0.9, 0.95]
INTERVALS = [2, 3, 5]


class ExecutionSummary(object):
    def __init__(self, actual, predicted):
        actual, predicted = cut(actual, predicted)
        self.actual, self.predicted = tuple(TimeSeries(data) for data in [actual, predicted])
        self.qdiff = self.actual.qdiff

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
        index = MultiIndex.from_tuples(index, names=['board', 'q'])

        return DataFrame(data, index=index)

    def overloads(self, size, interval):
        bound = size * self.qdiff
        true_overloads = self.actual.overloads(bound)
        predicted_overloads = self.predicted.overloads(bound)
        detected_overloads = 0
        for overload in true_overloads:
            quality_interval = self.predicted.quality_interval(overload, interval)
            if len(quality_interval.overloads(bound)) > 0:
                detected_overloads += 1

        tp_count = detected_overloads
        fp_count = abs(len(predicted_overloads) - detected_overloads)
        overload_count = len(true_overloads)

        if overload_count == 0:
            return 100, 0, 0

        tp_percentage, fp_percentage = tuple(100 * float(count) / overload_count for count in [tp_count, fp_count])
        return tp_percentage, fp_percentage, overload_count

    def ape_series(self):
        quality = ForecastQuality(self.actual.data, self.predicted.data)
        return quality.ape_series()
