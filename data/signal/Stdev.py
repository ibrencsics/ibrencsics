import statistics as stats
import math as math
import pandas as pd

class Stdev:

    def calculate(self, series, time_period):
        history = []  # history of prices
        sma_values = []  # to track moving average values for visualization purposes
        stddev_values = []  # history of computed stdev values

        for val in series:
            history.append(val)
            if len(history) > time_period:  # we track at most 'time_period' number of prices
                del (history[0])

            sma = stats.mean(history)
            sma_values.append(sma)

            variance = 0  # variance is square of standard deviation
            for hist_price in history:
                variance = variance + ((hist_price - sma) ** 2)

            stdev = math.sqrt(variance / len(history))

            stddev_values.append(stdev)

        return pd.Series(data=stddev_values, index=series.index, name='stdev' + str(time_period))