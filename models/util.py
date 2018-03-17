from statsmodels.tsa.stattools import adfuller


def is_stationary(ts):
    results = adfuller(ts, regression='ct')
    return results[0] < results[4]['5%']
