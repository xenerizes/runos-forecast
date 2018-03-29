import pandas as pd


class ControlStats(object):
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
        return pd.DataFrame(data, index=self.frame.index)
