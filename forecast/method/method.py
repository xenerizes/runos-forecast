import logging
from time import strftime, localtime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from forecast.algorithm import AggregationAlgorithm

TIME_FORMAT = "%Y-%m-%d_%H-%M"


def print_time_summary(ts):
    res = pd.Series([ts.min(), ts.max(), ts.mean(), ts.median()],
                    index=['Min', 'Max', 'Mean', 'Median'])
    logging.info(res.__str__())


class LoadForecastMethod(object):
    def __init__(self, storage, algo_class, model_class, opts):
        self.algo_class = algo_class
        self.model_class = model_class
        self.opts = opts
        self.storage = storage

    def run(self):
        quality_array = []
        full_time_data = []
        for idx, ts in enumerate(self.storage):
            logging.info('Starting forecasting method for DataFrame {}...'.format(idx))
            try:
                sw_algos = {sw: self.algo_class(self.model_class, data, self.opts)
                            for sw, data in ts.switch_load().items()}
                for sw, algo in sw_algos.items():
                    logging.info('Forecasting load from switch {}...'.format(sw))
                    algo.run()
                    logging.info('Forecast quality for series {}, switch {}:'.format(idx, sw))
                    algo.print_quality()
                    full_time_data += algo.time_stats()
                lm = AggregationAlgorithm(ts, [a.forecast for a in sw_algos.values()], self.opts)
                logging.info('Forecasting summary load...')
                lm.run()
                logging.info('Summary quality information for series {}'.format(idx))
                lm.print_quality()
                lm.print_detection_quality()

                quality_array.append(np.concatenate([algo.quality_stats() for algo in sw_algos.values()]))
                quality_array.append(lm.quality_stats())

                ax = lm.data.plot(figsize=(20, 15), grid=True, title=str(idx), label='actual')
                lm.forecast.plot(ax=ax, grid=True, label='predicted')
                plt.savefig('figure-{}-{}.png'.format(idx, strftime(TIME_FORMAT, localtime())),
                            bbox_inches='tight')
                plt.close()

            except Exception as e:
                logging.error('An error occurred while processing DataFrame {}, skipping...'.format(idx))
                logging.error(str(e))
                continue

        quality_frame = pd.Series(np.concatenate(quality_array))
        quality_frame.hist(figsize=(20, 15), grid=True)
        plt.savefig('hist-{}.png'.format(strftime(TIME_FORMAT, localtime())), bbox_inches='tight')
        plt.close()

        time_ts = pd.Series(full_time_data)
        logging.info('Fitting time information')
        print_time_summary(time_ts)
        time_ts.hist(figsize=(20, 15), grid=True)
        plt.savefig('time-{}.png'.format(strftime(TIME_FORMAT, localtime())), bbox_inches='tight')
        plt.close()
