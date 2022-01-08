import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DualMovingAverageStrategy:

    def calculate(self, series):
        signals = self.double_moving_average(series, 20, 100)
        self.visualize(series, signals)

    def double_moving_average(self, series, short_window, long_window):
        signals = pd.DataFrame(index=series.index)
        signals['signal'] = 0.0
        signals['short_mavg'] = series.rolling(window=short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = series.rolling(window=long_window, min_periods=1, center=False).mean()
        signals['signal'][short_window:] = \
            np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['orders'] = signals['signal'].diff()
        return signals

    def visualize(self, series, signals):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Google price in $')
        series.plot(ax=ax1, color='g', lw=.5)
        signals["short_mavg"].plot(ax=ax1, color='r', lw=2.)
        signals["long_mavg"].plot(ax=ax1, color='b', lw=2.)

        ax1.plot(signals.loc[signals.orders == 1.0].index,
                 series[signals.orders == 1.0],
                 '^', markersize=7, color='k')

        ax1.plot(signals.loc[signals.orders == -1.0].index,
                 series[signals.orders == -1.0],
                 'v', markersize=7, color='k')

        plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
        plt.title("Double Moving Average Trading Strategy")

        plt.show()
