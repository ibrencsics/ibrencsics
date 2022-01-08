import pandas as pd

from learn.signal.Stdev import Stdev

'''
The Exponential Moving Average (EMA) represents
 an average of prices, but places more weight on recent prices. The
 weighting applied to the most recent price depends on the selected
 period of the moving average. The shorter the period for the EMA,
 the more weight that will be applied to the most recent price.

EMA = ( P - EMAp ) * K + EMAp

Where:

P = Price for the current period
EMAp = the Exponential moving Average for the previous period
K = the smoothing constant, equal to 2 / (n + 1)
n = the number of periods in a simple moving average roughly approximated by the EMA
'''

class Ema:

    def __init__(self):
        self.stdev = Stdev()

    def calculate(self, series, period, k):
        ema_values = self.calculateInternal(series, period, k)
        return pd.Series(data=ema_values, index=series.index, name='ema' + str(period))

    def calculateWithStdev(self, series, period_ema, k, period_stdev):
        stdev = self.stdev.calculate_manual(series, period_stdev).to_numpy()
        ema_values, stdev_factor_values = self.calculateInternalWithStdev(series, period_ema, k, stdev)

        ema_series = pd.Series(data=ema_values, index=series.index, name='ema' + str(period_ema))
        stdev_factor_series = pd.Series(data=stdev_factor_values, index=series.index, name='stdev_factor' + str(period_stdev))
        return ema_series, stdev_factor_series

    def calculateInternal(self, series, period, k):
        K = k / (period + 1)  # smoothing constant
        ema_p = 0

        ema_values = []
        for val in series:
            if ema_p == 0:  # first observation, EMA = current-price
                ema_p = val
            else:
                ema_p = (val - ema_p) * K + ema_p

            ema_values.append(ema_p)

        return ema_values

    def calculateInternalWithStdev(self, series, period, k, stdev):
        K = k / (period + 1)  # smoothing constant
        ema_p = 0

        ema_values = []
        stdev_factor_values = []
        stdev_mean = stdev.mean()

        for i in range(len(series)):
            val = series[i]

            stdev_factor = stdev[i] / stdev_mean
            if stdev_factor == 0:
                stdev_factor = 1

            if ema_p == 0:  # first observation, EMA = current-price
                ema_p = val
            else:

                ema_p = (val - ema_p) * K * stdev_factor + ema_p

            ema_values.append(ema_p)
            stdev_factor_values.append(stdev_factor)

        return ema_values, stdev_factor_values