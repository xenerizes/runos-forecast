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

    def reselect_model(self):
        return self.select_model()

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

    def get_quality(self):
        if self.summary is None:
            self._set_summary()
        return self.summary.quality()

    def get_detection_quality(self):
        if self.summary is None:
            self._set_summary()
        return self.summary.detection_summary()

    def quality_stats(self):
        if self.summary is None:
            self._set_summary()
        return self.summary.ape_series()

    def time_stats(self):
        return self.time

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
                step_time = time.time()
                if self.needs_selection():
                    logging.debug('Model selection required, calculating...')
                    order = self.select_model()
                logging.debug('Model fitting...')
                try:
                    self.fit_model(order)
                except Exception:
                    try:
                        logging.warning('Error fitting model. Trying to re-select order')
                        order = self.select_model()
                        self.fit_model(order)
                    except Exception:
                        try:
                            logging.warning('Error fitting model. Trying to fit with higher d')
                            p, d, q = self.model.order
                            order = p, d + 1, q
                            self.fit_model(order)
                        except Exception:
                            logging.warning('Error fitting model. Trying to use another IC')
                            order = self.reselect_model()
                            self.fit_model(order)
                order = self.model.order
                logging.debug('Updating forecast results...')
                self.step()
                self.time.append(time.time() - step_time)
                logging.debug('Shifting history window...')
                self.next()
                logging.debug('Step {} completed\n'.format(steps))
            except KeyboardInterrupt:
                print('Interrupted')
