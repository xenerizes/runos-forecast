from pandas import Series
from IPython.display import display

from ..summary import ExecutionSummary


class BaseAlgorithm(object):
    def __init__(self, klass, data, interval, history_len):
        self.data = data
        self.forecast = Series()
        self.model = None
        self.model_class = klass
        self.interval = interval
        self.history_len = history_len
        self.history = None
        self.start = 0
        self.end = self.history_len
        self.summary = None

    def _set_summary(self):
        self.summary = ExecutionSummary(self.data, self.forecast)

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

    def print_quality(self):
        if self.summary is None:
            self._set_summary()
        display(self.summary.quality())

    def print_detection_quality(self):
        if self.summary is None:
            self._set_summary()
        display(self.summary.detection_summary())

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
                break
            except KeyboardInterrupt:
                print('Interrupted')
