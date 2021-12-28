import math
import statistics as stats
import pandas as pd

from data.signal.Sma import Sma
from data.signal.Stdev import Stdev


class Bbands:

    def __init__(self):
        self.sma = Sma()
        self.stdev = Stdev()

    def calculate(self, series, time_period, stdev_factor):
        sma_series = self.sma.calculate(series, time_period)
        stdev_series = self.stdev.calculate(series, time_period)
        lower_series = sma_series - stdev_factor * stdev_series
        lower_series.name = 'lower' + str(time_period)
        upper_series = sma_series + stdev_factor * stdev_series
        upper_series.name = 'upper' + str(time_period)

        # history = []
        # sma_values = []
        # upper_band = []
        # lower_band = []
        #
        # for val in series:
        #     history.append(val)
        #     if len(history) > time_period:
        #         del (history[0])
        #
        #     sma = stats.mean(history)
        #     sma_values.append(sma)  # simple moving average or middle band
        #
        #     variance = 0  # variance is the square of standard deviation
        #     for hist_price in history:
        #         variance = variance + ((hist_price - sma) ** 2)
        #
        #     stdev = math.sqrt(variance / len(history))  # use square root to get standard deviation
        #
        #     upper_band.append(sma + stdev_factor * stdev)
        #     lower_band.append(sma - stdev_factor * stdev)
        #
        # sma_series = pd.Series(data=sma_values, index=series.index, name='sma' + str(time_period))
        # lower_series = pd.Series(data=lower_band, index=series.index, name='lower')
        # upper_series = pd.Series(data=upper_band, index=series.index, name='upper')

        return sma_series, lower_series, upper_series
