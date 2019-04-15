from argparse import ArgumentParser


def make_large_parser():
    parser = ArgumentParser()
    parser.add_argument('file', type=str, help='CSV input')
    parser.add_argument('--dc', '-d', action='store_true', help='Specify if input is not Runos')
    parser.add_argument('interval', type=int, help='F')
    parser.add_argument('hist_len', type=int, help='W')
    parser.add_argument('k', type=int, default=0, help='k')
    parser.add_argument('corr_interval', type=int, default=0, help='M')
    parser.add_argument('-s', type=str, help='JSON with predefined models')
    parser.add_argument('-c', action='store_true', help='Count model changes and steps')
    return parser
