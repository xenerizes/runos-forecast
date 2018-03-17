#!/usr/bin/env python3

import argparse
import sys

import matplotlib.pyplot as plt
import pandas as pd

from forecast.cstats import ControlStats


def plot(frame):
    frame.plot()
    plt.show(block=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file', type=str
    )
    opts = parser.parse_args(sys.argv[1:])

    frame = pd.read_csv(opts.file, index_col=[0])
    stats = ControlStats(frame)
    aggregated = stats.aggregate()
    plot(aggregated.diff())
