class Metric(object):
    def __init__(self, func, k):
        self.metric = func
        self.values = []
        self.k = k

    def append(self, actual, predicted):
        value = self.metric(actual, predicted)
        self.values.append(value)

    def clear(self):
        self.values.clear()

    def diff(self):
        if len(self.values) == 0:
            return 0
        return max(self.values) / min(self.values)

    def is_bad(self):
        return self.diff() > self.k
