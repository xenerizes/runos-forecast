from .util import convert_time, infer_freq

HIGHER_QUANTILE = 0.95
LOWER_QUANTILE = 1 - HIGHER_QUANTILE


class TimeSeries(object):
    def __init__(self, data):
        if data.index.freq is None:
            freq = infer_freq(data.index)
            data = data.asfreq(freq)

        self.data = data
        self.qdiff = data.quantile(HIGHER_QUANTILE) - data.quantile(LOWER_QUANTILE)

    def is_overload(self, point, bound):
        if self.data.index[0] == point:
            return False

        previous = point - point.freq
        return self.data[previous] < bound <= self.data[point]

    def overloads(self, bound):
        return [point for point in self.data.index if self.is_overload(point, bound)]

    def quality_interval(self, point, interval):
        start_time = (point - 2 * interval - point.freq)
        end_time = (point + 2 * interval)
        start_time, end_time = convert_time(start_time, end_time)
        data = self.data.between_time(start_time, end_time)
        return TimeSeries(data)
