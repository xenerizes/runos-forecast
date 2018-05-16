from pandas import Series
from ..summary import ExecutionSummary


class BaseAlgorithm(object):
    def __init__(self, data, interval, history_len):
        self.data = data
        self.forecast = Series()
        self.model = None
        self.interval = interval
        self.history_len = history_len
        self.history = None
        self.start = 0
        self.end = self.history_len

    def predict(self, interval):
        return self.model.predict(interval)

    def select_model(self):
        pass

    def fit_model(self):
        pass

    def notify_controller(self):
        pass

    def needs_selection(self):
        return True

    def needs_fitting(self):
        return True

    def is_overload(self):
        pass

    def step(self):
        predicted = self.predict(self.interval)
        self.forecast = self.forecast.append(predicted)
        if self.is_overload():
            self.notify_controller()

    def next(self):
        pass

    def print_summary(self):
        summary = ExecutionSummary(self.data, self.forecast)
        overloads = summary.overloads(600, 5)
        false_positives = summary.false_positives(600, 5)
        print(summary.quality())
        print("Overloads: {}".format(overloads))
        print("FP: {}".format(false_positives))

    def run(self):
        while self.start != self.end:
            try:
                self.history = self.data.iloc[self.start:self.end]
                if self.history.empty:
                    return
                if self.needs_selection():
                    self.select_model()
                if self.needs_fitting():
                    self.fit_model()
                self.step()
                self.next()
            except KeyboardInterrupt:
                print('Interrupted')
