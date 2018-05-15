from pandas import Series


class BaseAlgorithm(object):
    def __init__(self, data, interval, history_len):
        self.data = data
        self.forecast = Series()
        self.model = None
        self.interval = interval
        self.history_len = history_len
        self.history = data.head(history_len)
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
        self.forecast += self.predict(self.interval)
        if self.is_overload():
            self.notify_controller()

    def next(self):
        return 0, 0

    def run(self):
        try:
            self.history = self.data.iloc(self.start, self.end)
            if self.history.empty:
                return 
            if self.needs_selection():
                self.select_model()
            if self.needs_fitting():
                self.fit_model()
            self.step()
        except KeyboardInterrupt:
            print('Interrupted')
