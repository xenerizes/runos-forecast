from argparse import ArgumentParser
from forecast.loader import ControlStats, DcStats
import pandas as pd
import sys

def make_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'file', type=str, help='CSV input'
    )
    parser.add_argument(
        '--dc', action='store_true', help='Specify if input is not Runos'
    )
    return parser


def parse():
    parser = make_parser()
    opts = parser.parse_args(sys.argv[1:])

    frame = pd.read_csv(opts.file, index_col=[0])
    if opts.dc:
        return DcStats(frame)
    else:
        return ControlStats(frame)
