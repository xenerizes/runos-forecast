import pandas as pd

from ..storage import StatsStorage


class DcStats(StatsStorage):
    def __init__(self, frame):
        self.col_names = ['devname', 'infname', 'inbits', 'outbits']
        self.frame = frame.filter(items=self.col_names, axis=1)
        self.frame.index = pd.to_datetime(self.frame.index)
        self.frame.inbits = self.frame.inbits.astype('float64')
        self.frame.outbits = self.frame.outbits.astype('float64')

    def columns(self, names):
        cols = []
        for column in self.frame.columns:
            if column in names:
                cols.append(column)
        return cols

    def dev_list(self):
        filtered = self.frame.devname.drop_duplicates()
        return filtered.reset_index().drop('time', axis=1).devname

    def inf_list(self):
        filtered = self.frame.infname.drop_duplicates()
        return filtered.reset_index().drop('time', axis=1).infname

    def summary(self, type=0):
        if type is 1:
            return self.inf_summary()
        data = list()
        for dev in self.dev_list():
            dev_records = self.frame.loc[self.frame['devname'] == dev]
            data.append(dev_records)
        return data

    def inf_summary(self):
        data = list()
        for inf in self.inf_list():
            inf_records = self.frame.loc[self.frame['infname'] == inf]
            new_index = pd.date_range(start='2007-10-19 20:00', periods=len(inf_records), freq='15T')
            inf_records.index = new_index
            data.append(inf_records)
        return data

    def to_frame_list(self):
        storage = []
        devices = self.summary()
        for dev_data, dev_name in zip(devices, self.dev_list()):
            stats = DcStats(dev_data)
            storage += stats.inf_summary()
        return storage
