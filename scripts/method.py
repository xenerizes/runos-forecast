# !/usr/bin/env python3

import logging
from sys import argv, warnoptions
from pandas import read_csv

from forecast.algorithm import SimpleAlgorithm, CorrectiveAlgorithm
from forecast.loader.stats import *
from forecast.models.arima import ARIMAModel
from forecast.method import LoadForecastMethod
from scripts.util import make_large_parser

LOGGING_FORMAT = '%(levelname)s: %(message)s'


def load(opts):
    frame = read_csv(opts.file, index_col=[0])
    if opts.dc:
        helper = DcStatsHelper(frame)
        return [DcStats(f) for f in helper.inf_summary()]
    else:
        return [ControlStats(frame)]


def get_ts(ts):
    return ts.load()


def parse():
    parser = make_large_parser()
    opts = parser.parse_args(argv[1:])
    data = load(opts)
    method = LoadForecastMethod(data, CorrectiveAlgorithm, ARIMAModel, opts)
    method.run()


if __name__ == '__main__':
    if not warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    logging.basicConfig(format=LOGGING_FORMAT, level='DEBUG')
    parse()
