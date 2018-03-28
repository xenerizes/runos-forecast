import pandas as pd


class DcStats(object):
    def __init__(self, frame):
        self.frame = frame
        self.col_names = ['devname', 'infname', 'inbits', 'outbits']

    def columns(self, names):
        cols = []
        for column in self.frame.columns:
            if column in names:
                cols.append(column)
        return cols

    def locate(self, dev, inf):
        pass

    def summary(self):
        pass
