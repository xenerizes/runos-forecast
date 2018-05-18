from pandas import Series


def cut(ts1, ts2):
    common_start = max(ts1.index[0], ts2.index[0])
    common_end = min(ts1.index[-1], ts2.index[-1])
    return tuple(series[common_start:common_end] for series in [ts1, ts2])


def convert_time(start, end):
    return tuple(point.to_pydatetime().time() for point in [start, end])


def infer_freq(index):
    gaps = Series(index[1:]) - Series(index[:-1])
    gaps_count = gaps.value_counts()
    return gaps_count.index[0]
