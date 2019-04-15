from forecast.algorithm import AggregationAlgorithm


class LoadForecastMethod(object):
    def __init__(self, storage, algo_class, model_class, *args):
        self.algo_class = algo_class
        self.model_class = model_class
        self.params = args
        self.storage = storage

    def run(self):
        for ts in self.storage:
            sw_algos = [self.algo_class(self.model_class, data[100:], *self.params)
                        for data in ts.switch_load().values()]
            for algo in sw_algos:
                algo.run()
                algo.print_quality()
            lm = AggregationAlgorithm(ts, [a.forecast for a in sw_algos], self.params[1])
            lm.run()
            lm.print_detection_quality()
            break
