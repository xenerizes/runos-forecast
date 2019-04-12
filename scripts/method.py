# !/usr/bin/env python3

from sys import argv
from pandas import read_csv

from forecast.algorithm.simple import SimpleAlgorithm
from forecast.loader import ControlStats, DcStats
from forecast.models.arima import ARIMAModel
from scripts.util import make_parser


def run(data, interval, history_len):
    algorithm = SimpleAlgorithm(ARIMAModel, data, interval, history_len)

    algorithm.run()
    algorithm.print_summary()


def load(opts):
    frame = read_csv(opts.file, index_col=[0])
    if opts.dc:
        return DcStats(frame)
    else:
        return ControlStats(frame)


def get_ts(ts):
    outmean = ts.outbits.mean()
    inmean = ts.inbits.mean()
    if outmean > inmean:
        return ts.outbits
    else:
        return ts.inbits


def parse():
    parser = make_parser()
    opts = parser.parse_args(argv[1:])
    data = load(opts).to_frame_list()
    hist_len = 50
    interval = 5
    for ts in data:
        to_run = get_ts(ts)
        run(to_run, interval, hist_len)
        break


if __name__ == '__main__':
    parse()
