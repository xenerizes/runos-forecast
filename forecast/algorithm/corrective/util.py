def corr_dist(series1, series2):
    return 1 - series1.corr(series2)
