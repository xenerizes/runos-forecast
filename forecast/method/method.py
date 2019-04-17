import logging
from time import strftime, localtime
from pandas import DataFrame
import matplotlib.pyplot as plt

from forecast.algorithm import AggregationAlgorithm

TIME_FORMAT = "%Y-%m-%d_%H-%M"


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
                lm.print_detection_quality()

                algo_quality = {'{}'.format(sw): sw_algos[sw].quality_stats() for sw in sw_algos.keys()}
                algo_quality['full'] = lm.quality_stats()
                quality_frame = DataFrame(algo_quality)
                quality_frame.hist(figsize=(20, 15), grid=True)
                plt.savefig('hist-{}-{}.png'.format(idx, strftime(TIME_FORMAT, localtime())),
                            bbox_inches='tight')
                plt.close()

                lm.data.plot(figsize=(20, 15), grid=True, title=str(idx))
                lm.forecast.plot(figsize=(20, 15), grid=True, title=str(idx))
                plt.savefig('figure-{}-{}.png'.format(idx, strftime(TIME_FORMAT, localtime())),
                            bbox_inches='tight')

            except Exception as e:
                logging.error('An error occurred while processing DataFrame {}, skipping...'.format(idx))
                logging.error(str(e))
                continue
