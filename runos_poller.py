#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
import requests
from time import sleep
from datetime import datetime


def make_parser():
    parser = ArgumentParser(
        prog='./runos_poller.py',
        description='Polling runos for switches control stats and sending parsed data to sdtout',

    )
    parser.add_argument(
        '--ip', type=str, default='127.0.0.1',
        help='Runos address'
    )
    parser.add_argument(
        '--port', '-p', type=int, default=8000,
        help='Runos REST port'
    )
    parser.add_argument(
        '--interval', '-i', type=int, default=30,
        help='Polling interval in seconds'
    )
    return parser


class Poller(object):
    def __init__(self, ip, port, interval):
        self.ctrl_ip = ip
        self.ctrl_port = port
        self.interval = interval

    def poll(self):
        while True:
            time = self.get_time()
            response = self.request_stats()
            data = self.json_to_csv(time, response)
            print(data)
            sleep(self.interval)

    def request_stats(self):
        req = requests.get('http://{}:{}/switches/controlstats/'.format(self.ctrl_ip, self.ctrl_port))
        if req.status_code != 200:
            return None

        return req.json()

    @staticmethod
    def json_to_csv(time, data):
        if data is None:
            return '{}'.format(time)
        switches = data['control_stats']
        if switches is None:
            return '{}'.format(time)

        csv_str = ''
        for switch in switches:
            rx = switch['rx_ofpackets']
            tx = switch['tx_ofpackets']
            pi = switch['pkt_in_ofpackets']
            csv_str += ',{},{},{}'.format(rx, tx, pi)

        return '{}{}'.format(time, csv_str)

    @staticmethod
    def get_time():
        return datetime.now().isoformat()


def start():
    parser = make_parser()
    opts = parser.parse_args(sys.argv[1:])
    poller = Poller(opts.ip, opts.port, opts.interval)
    poller.poll()


if __name__ == "__main__":
    start()
