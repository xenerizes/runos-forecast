import pandas as pd
import numpy as np
from ..storage import StatsStorage


def _guess_seconds(index):
    return np.min(index[1:] - index[:-1]).seconds


class ControlStats(StatsStorage):
    def __init__(self, frame):
        self.frame = frame
        self.col_postfix = ['rx', 'tx', 'pi']
        self.frame.index = pd.to_datetime(self.frame.index)
        self.frame.index = pd.date_range(start=frame.index[0],
                                         periods=len(frame),
                                         freq='{}S'.format(_guess_seconds(self.frame.index)))

    def sum_columns(self, columns):
        series = pd.Series(0, index=self.frame.index)
        for column in columns:
            series += self.frame[column]
        return series

    def columns(self, postfix):
        cols = []
        for column in self.frame.columns:
            if postfix in column:
                cols.append(column)
        return cols

    def aggregate(self):
        data = dict()
        for postfix in self.col_postfix:
            columns = self.columns(postfix)
            data[postfix] = self.sum_columns(columns)
        return data

    def to_data_frame(self):
        return pd.DataFrame(self.aggregate(), index=self.frame.index)

    def to_frame_list(self):
        return self.aggregate()

    def switch_load(self):
        return {int(column[:-2]): self.frame[column].astype('float64') for column in self.columns('pi')}

    def load(self):
        return self.aggregate()['rx'].astype('float64')
