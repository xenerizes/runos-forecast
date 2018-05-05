from pandas import Series


class BaseAlgorithm(object):
    def __init__(self, storage, interval, history_len):
        self.storage = storage
        self.forecast = Series()
        self.model = None
        self.interval = interval
        self.history_len = history_len
        self.history = None

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
        self.forecast += self.predict(self.interval)
        if self.is_overload():
            self.notify_controller()

    def run(self, start_time):
        time = start_time
        try:
            self.history = self.storage.get(time - self.history_len, time)
            if self.needs_selection():
                self.select_model()
            if self.needs_fitting():
                self.fit_model()
            self.step()
        except KeyboardInterrupt:
            print('Interrupted')
