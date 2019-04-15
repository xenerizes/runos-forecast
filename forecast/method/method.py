class LoadForecastMethod(object):
    def __init__(self, storage, algo_class, model_class, *args):
        self.algo_class = algo_class
        self.model_class = model_class
        self.params = args
        self.storage = storage

    def run(self):
        for ts in self.storage:
            data = ts.load()
            algo = self.algo_class(self.model_class, data, *self.params)
            algo.run()
            algo.print_summary()
            break
