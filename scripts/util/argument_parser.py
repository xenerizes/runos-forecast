from argparse import ArgumentParser
import sys


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        'file', type=str, help='CSV input'
    )
    parser.add_argument(
        '--dc', action='store_true', help='Specify if input is not Runos'
    )
    return parser.parse_args(sys.argv[1:])
