# !/usr/bin/env python3

from sys import argv, warnoptions
from pandas import read_csv

from forecast.algorithm.simple import SimpleAlgorithm
from forecast.loader.stats import *
from forecast.models.arima import ARIMAModel
from forecast.method import LoadForecastMethod
from scripts.util import make_parser


def run(data, interval, history_len):
    algorithm = SimpleAlgorithm(ARIMAModel, data, interval, history_len)

    algorithm.run()
    algorithm.print_quality()


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
    parser = make_parser()
    opts = parser.parse_args(argv[1:])
    data = load(opts)
    hist_len = 50
    interval = 5
    method = LoadForecastMethod(data, SimpleAlgorithm, ARIMAModel, interval, hist_len)
    method.run()


if __name__ == '__main__':
    if not warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    parse()
