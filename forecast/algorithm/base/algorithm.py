class BaseAlgorithm(object):
    def __init__(self):
        self._history = None
        self._model = None
        self._forecast = None
        self._interval = 0

    def predict(self):
        pass

    def select_model(self):
        pass

    def fit_model(self):
        pass

    def notify(self):
        pass

    def needs_selection(self):
        pass

    def needs_fitting(self):
        pass

    def is_overload(self):
        pass

    def step(self):
        self.predict()
        if self.is_overload():
            self.notify()

    def run(self):
        try:
            while True:
                if self.needs_selection():
                    self.select_model()
                if self.needs_fitting():
                    self.fit_model()
                self.step()
        except KeyboardInterrupt:
            print('Interrupted')
