from forecast.models.base.quality import ForecastQuality


class ExecutionSummary(object):
    def __init__(self, actual, predicted):
        self.actual = actual
        self.predicted = predicted
        self.cut()

    def quality(self):
        return ForecastQuality(self.actual, self.predicted).summary()

    def cut(self):
        common_start = max(self.actual.index[0], self.predicted.index[0])
        common_end = min(self.actual.index[-1], self.predicted.index[-1])
        self.actual = self.actual[common_start:common_end].bfill()
        self.predicted = self.predicted[common_start:common_end].bfill()

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

        print("last elem is: ", self.predicted.index[-1])
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
