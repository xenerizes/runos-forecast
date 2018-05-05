#!/usr/bin/env python3

from .util import make_parser
import sys
import math

sys.path += '../' + sys.argv[0]

import matplotlib.pyplot as plt
import pandas as pd
from forecast.loader import ControlStats, DcStats


def shape(x):
    ncols = math.ceil(pow(x, 0.5))
    if ncols > 4:
        ncols = 4
    nrows = math.ceil(x / ncols)
    return int(ncols), int(nrows)


def add_subplots(datasets, time_visibility=False):
    ncols, nrows = shape(len(datasets))
    for idx, dataset in enumerate(datasets):
        title = '{}: {} - {}'.format(idx, dataset.devname[0], dataset.infname[0])
        sp = plt.subplot(nrows, ncols, idx + 1)
        dataset.plot(ax=sp, grid=True, title=title)
        sp.get_xaxis().set_visible(time_visibility)


def plot_dc(frame, time_visibility=False, type=0):
    stats = DcStats(frame).summary(type)
    plt.subplots_adjust(left=0.05, bottom=0.1,
                        right=0.98, top=0.95)
    add_subplots(stats, time_visibility)
    plt.show(block=True)


def plot_runos(frame):
    stats = ControlStats(frame)
    aggregated = stats.to_data_frame()
    aggregated.diff().plot(grid=True)
    plt.show(block=True)

if __name__ == '__main__':
    parser = make_parser()
    opts = parser.parse_args(sys.argv[1:])

    frame = pd.read_csv(opts.file, index_col=[0])
    if opts.dc:
        plot_dc(frame)
    else:
        plot_runos(frame)
