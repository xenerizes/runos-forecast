from argparse import ArgumentParser


def make_large_parser():
    parser = ArgumentParser()
    parser.add_argument('file', type=str, help='CSV input')
    parser.add_argument('--dc', '-d', action='store_true', help='Specify if input is not Runos')
    parser.add_argument('--interval', '-F', type=int, required=True, help='F')
    parser.add_argument('--hist_len', '-W', type=int, required=True, help='W')
    parser.add_argument('--k', type=float, default=1, help='k')
    parser.add_argument('--corr_interval', '-M', type=int, default=0, help='M')
    parser.add_argument('-s', type=str, help='JSON with predefined models')
    parser.add_argument('-c', action='store_true', help='Count model changes and steps')
    return parser
