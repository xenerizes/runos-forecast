from forecast.models.base.quality import ForecastQuality
import pandas as pd


OVERLOAD_SIZES = [0.75, 0.8, 0.85, 0.9, 0.95]
INTERVALS = [2, 3, 5]


class ExecutionSummary(object):
    def __init__(self, actual, predicted):
        self.actual = actual
        self.predicted = predicted
        self.cut()

    def quality(self):
        result = ForecastQuality(self.actual, self.predicted).summary()
        return result.to_frame("Value")

    def cut(self):
        common_start = max(self.actual.index[0], self.predicted.index[0])
        common_end = min(self.actual.index[-1], self.predicted.index[-1])
        self.actual = self.actual[common_start:common_end]
        self.predicted = self.predicted[common_start:common_end]

    def detection_summary(self):
        qdiff = self.actual.quantile(0.95) - self.actual.quantile(0.05)

        overloads = []
        fps = []
        index = []
        for size in OVERLOAD_SIZES:
            for interval in INTERVALS:
                overloads.append(self.overloads(qdiff * size, interval))
                fps.append(self.false_positives(qdiff * size, interval))
                index.append((size, interval))

        data = { "TP": overloads, "FP": fps }
        index = pd.MultiIndex.from_tuples(index, names=['size', 'interval'])
        return pd.DataFrame(data, index=index)

    def overloads(self, board, interval):
        overloads = 0
        predicted = 0
        for point in self.actual.index:
            if self.actual[point] < board:
                continue

            if self.actual[point - point.freq] >= board:
                continue

            overloads += 1
            start_time = (point - 2 * interval).to_pydatetime()
            end_time = (point + 2 * interval).to_pydatetime()
            observe = self.predicted.between_time(start_time.time(), end_time.time())

            for value in observe:
                if value >= board:
                    predicted += 1
                    break

        return 0 if overloads is 0 else 100.0 * predicted / overloads

    def false_positives(self, board, interval):
        overloads = 0
        false_overloads = 0
        for point in self.actual.index:
            if self.actual[point] < board:
                continue
            if self.actual[point - point.freq] < board:
                overloads += 1

        for point in self.predicted.index:
            if self.predicted[point] < board:
                continue

            if self.predicted[point - point.freq] >= board:
                continue

            start_time = (point - 2 * interval).to_pydatetime()
            end_time = (point + 2 * interval).to_pydatetime()
            observe = self.actual.between_time(start_time.time(), end_time.time())

            overload = False
            for value in observe:
                if value > board:
                    overload |= True
                    break
            if not overload:
                false_overloads += 1

        return 0 if overloads is 0 else 100.0 * false_overloads / overloads
