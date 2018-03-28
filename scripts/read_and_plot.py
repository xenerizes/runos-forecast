#!/usr/bin/env python3

import argparse
import sys

import matplotlib.pyplot as plt
import pandas as pd

from forecast.cstats import ControlStats, DcStats


def plot(frame):
    frame.plot()
    plt.show(block=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file', type=str, help='CSV input'
    )
    parser.add_argument(
        '--dc', action='store_true', help='Specify if input is not Runos'
    )
    opts = parser.parse_args(sys.argv[1:])

    frame = pd.read_csv(opts.file, index_col=[0])
    if opts.dc:
        stats = DcStats(frame)
        plot(stats.summary())
    else:
        stats = ControlStats(frame)
        aggregated = stats.aggregate()
        plot(aggregated.diff())
