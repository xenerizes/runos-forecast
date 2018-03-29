from . import Storage, TimeRange

class BaseAlgorithm(object):
    def __init__(self):
        self._history = Storage(None)
        self._forecast = Storage(None)
        self._model = None
        self._interval = 0
        self._time = 0

    def predict(self, interval):
        pass

    def select_model(self):
        pass

    def fit_model(self):
        pass

    def notify_controller(self):
        pass

    def needs_selection(self):
        pass

    def needs_fitting(self):
        pass

    def is_overload(self):
        pass

    def step(self, time_range):
        self._forecast[time_range] = self.predict(self._interval)
        if self.is_overload():
            self.notify_controller()

    def run(self):
        self._time = self._history.size()
        try:
            time_range = TimeRange(self._time, self._time + self._interval)
            if self.needs_selection():
                self.select_model()
            if self.needs_fitting():
                self.fit_model()
            self.step(time_range)
        except KeyboardInterrupt:
            print('Interrupted')
