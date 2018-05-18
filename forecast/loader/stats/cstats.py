import pandas as pd

from ..storage import StatsStorage


class ControlStats(StatsStorage):
    def __init__(self, frame):
        self.frame = frame
        self.col_postfix = ['rx', 'tx', 'pi']
        self.frame.index = pd.to_datetime(self.frame.index)

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
            aggregated = self.sum_columns(columns)
            data[postfix] = aggregated
        return data

    def to_data_frame(self):
        return pd.DataFrame(self.aggregate(), index=self.frame.index)

    def to_frame_list(self):
        return self.aggregate()
