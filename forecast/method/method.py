import logging
from time import strftime, localtime
from pandas import DataFrame

from forecast.algorithm import AggregationAlgorithm


class LoadForecastMethod(object):
    def __init__(self, storage, algo_class, model_class, opts):
        self.algo_class = algo_class
        self.model_class = model_class
        self.opts = opts
        self.storage = storage

    def run(self):
        for idx, ts in enumerate(self.storage):
            logging.info('Starting forecasting method for DataFrame {}...'.format(idx))
            try:
                sw_algos = {sw: self.algo_class(self.model_class, data, self.opts)
                            for sw, data in ts.switch_load().items()}
                for sw, algo in sw_algos.items():
                    logging.info('Forecasting load from switch {}...'.format(sw))
                    algo.run()
                    algo.print_quality()
                lm = AggregationAlgorithm(ts, [a.forecast for a in sw_algos.values()], self.opts)
                logging.info('Forecasting summary load...')
                lm.run()
                lm.print_quality()

                algo_quality = {'{}'.format(sw): sw_algos[sw].quality_stats() for sw in sw_algos.keys()}
                algo_quality['full'] = lm.quality_stats()
                quality_frame = DataFrame(algo_quality)
                quality_frame.to_csv('output-ts{}-{}'.format(idx, strftime("%Y-%m-%d.%H:%M", localtime())))
            except Exception as e:
                logging.error('An error occurred while processing DataFrame {}, skipping...'.format(idx))
                logging.error(str(e))
                continue
