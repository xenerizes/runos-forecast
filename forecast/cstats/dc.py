import pandas as pd


class DcStats(object):
    def __init__(self, frame):
        self.col_names = ['devname', 'infname', 'inbits', 'outbits']
        self.frame = frame.filter(items=self.col_names, axis=1)
        self.frame.index = pd.to_datetime(self.frame.index)

    def columns(self, names):
        cols = []
        for column in self.frame.columns:
            if column in names:
                cols.append(column)
        return cols

    def dev_list(self):
        filtered = self.frame.devname.drop_duplicates()
        return filtered.reset_index().drop('time', axis=1).devname

    def summary(self):
        data = list()
        for dev in self.dev_list():
            dev_records = self.frame.loc[self.frame['devname'] == dev]
            data.append(dev_records)
        return data
