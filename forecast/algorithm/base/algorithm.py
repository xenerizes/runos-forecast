import logging
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
        steps = 0
        while self.start != self.end:
            steps += 1
            logging.debug('Performing time step {}...'.format(steps))
            try:
                self.history = self.data.iloc[self.start:self.end]
                if self.history.empty:
                    return
                if self.needs_selection():
                    logging.debug('Model selection required, calculating...')
                    self.select_model()
                if self.needs_fitting():
                    logging.debug('Model fitting required, calculating...')
                    self.fit_model()
                logging.debug('Updating forecast results...')
                self.step()
                logging.debug('Shifting history window...')
                self.next()
                logging.debug('Step {} completed\n'.format(steps))
                break
            except KeyboardInterrupt:
                print('Interrupted')
