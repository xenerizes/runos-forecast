from pandas import Series


class BaseAlgorithm(object):
    def __init__(self, storage, interval, history_len):
        self._storage = storage
        self._forecast = Series()
        self._model = None
        self._interval = interval
        self._history_len = history_len
        self._history = None

    def predict(self, interval):
        return self._model.predict(interval)

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

    def step(self):
        self._forecast += self.predict(self._interval)
        if self.is_overload():
            self.notify_controller()

    def run(self, start_time):
        time = start_time
        try:
            self._history = self._storage.get(time - self._history_len, time)
            if self.needs_selection():
                self.select_model()
            if self.needs_fitting():
                self.fit_model()
            self.step()
        except KeyboardInterrupt:
            print('Interrupted')
