import logging
import time

from pandas import Series

from ..summary import ExecutionSummary


class BaseAlgorithm(object):
    def __init__(self, klass, data, opts):
        self.data = data
        self.forecast = Series()
        self.model = None
        self.model_class = klass
        self.interval = opts.interval
        self.history_len = opts.hist_len
        self.history = None
        self.start = 0
        self.end = self.history_len
        self.summary = None
        self.time = []

    def _set_summary(self):
        self.summary = ExecutionSummary(self.data, self.forecast)

    def predict(self, interval):
        return self.model.predict(interval)

    def select_model(self):
        pass

    def fit_model(self, order=None):
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
        logging.info(self.summary.quality().__str__())

    def print_detection_quality(self):
        if self.summary is None:
            self._set_summary()
        logging.info(self.summary.detection_summary().__str__())

    def quality_stats(self):
        if self.summary is None:
            self._set_summary()
        return self.summary.ape_series()

    def time_stats(self):
        return Series(self.time)

    def run(self):
        steps = 0
        order = None
        while self.start != self.end:
            steps += 1
            logging.debug('Performing time step {}...'.format(steps))
            try:
                self.history = self.data.iloc[self.start:self.end]
                if self.history.empty:
                    return
                step_time = 0
                if self.needs_selection():
                    order = self.model.order if self.model is not None else None
                    logging.debug('Model selection required, calculating...')
                    start_time = time.time()
                    self.select_model()
                    step_time += time.time() - start_time
                logging.debug('Model fitting required, calculating...')
                start_time = time.time()
                self.fit_model(order)
                step_time += time.time() - start_time
                self.time.append(step_time)
                order = None
                logging.debug('Updating forecast results...')
                self.step()
                logging.debug('Shifting history window...')
                self.next()
                logging.debug('Step {} completed\n'.format(steps))
            except KeyboardInterrupt:
                print('Interrupted')
