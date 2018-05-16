import unittest

import numpy as np
import pandas as pd

from forecast.loader import ControlStats


class ControlStatsTestCase(unittest.TestCase):
    def setUp(self):
        self.cstats = ControlStats()
        data = 100*np.random.randn(5, 6)
        index = pd.date_range('1/1/2000', periods=5)
        columns = ['1rx', '1tx', '1pi', '2rx', '2tx', '2pi']
        self.cstats.frame = pd.DataFrame(data, index=index, columns=columns)
        self.cstats.frame = self.cstats.diff()

    def testSumThreeColumns(self):
        columns = ['1pi', '2pi', '1tx']
        columns_sum = self.cstats.frame['1pi'] + self.cstats.frame['2pi'] + self.cstats.frame['1tx']
        aggregated = self.cstats.sum_columns(columns)
        self.assertTrue(aggregated.equals(columns_sum))

    def testExtractionByPostfix(self):
        postfix = 'rx'
        columns = self.cstats.columns(postfix)
        self.assertEqual(columns, ['1rx', '2rx'])

    def testStatsAggregation(self):
        sum_rx = self.cstats.frame['1rx'] + self.cstats.frame['2rx']
        sum_tx = self.cstats.frame['1tx'] + self.cstats.frame['2tx']
        sum_pi = self.cstats.frame['1pi'] + self.cstats.frame['2pi']
        sum_dict = {'rx': sum_rx, 'tx': sum_tx, 'pi': sum_pi}
        manual = pd.DataFrame(sum_dict, index=self.cstats.frame.index)
        aggregated = self.cstats.to_data_frame()
        self.assertTrue(manual.equals(aggregated))
