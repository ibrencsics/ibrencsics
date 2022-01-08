import pandas as pd
import matplotlib.pyplot as plt

class TurtleStrategy:

    def calculate(self, series):
        signals = self.turtle_trading(series, 50)
        self.visualize(series, signals)

    def turtle_trading(self, series, window_size):
        signals = pd.DataFrame(index=series.index)
        signals['orders'] = 0
        # window_size-days high
        signals['high'] = series.shift(1).rolling(window=window_size).max()
        # window_size-days low
        signals['low'] = series.shift(1).rolling(window=window_size).min()
        # window_size-days mean
        signals['avg'] = series.shift(1).rolling(window=window_size).mean()

        # entry rule : stock price > the higest value for window_size day
        #              stock price < the lowest value for window_size day

        signals['long_entry'] = series > signals.high
        signals['short_entry'] = series < signals.low

        # exit rule : the stock price crosses the mean of past window_size days.

        signals['long_exit'] = series < signals.avg
        signals['short_exit'] = series > signals.avg

        init = True
        position = 0
        for k in range(len(signals)):
            if signals['long_entry'][k] and position == 0:
                signals.orders.values[k] = 1
                position = 1
            elif signals['short_entry'][k] and position == 0:
                signals.orders.values[k] = -1
                position = -1
            # ib: this should be long_exit
            elif signals['short_exit'][k] and position > 0:
                signals.orders.values[k] = -1
                position = 0
            # ib: this should be short_exit
            elif signals['long_exit'][k] and position < 0:
                signals.orders.values[k] = 1
                position = 0
            else:
                signals.orders.values[k] = 0

        return signals

    def visualize(self, series, signals):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Google price in $')
        series.plot(ax=ax1, color='g', lw=.5)
        signals["high"].plot(ax=ax1, color='g', lw=.5)
        signals["low"].plot(ax=ax1, color='r', lw=.5)
        signals["avg"].plot(ax=ax1, color='b', lw=.5)

        ax1.plot(signals.loc[signals.orders == 1.0].index,
                 series[signals.orders == 1.0],
                 '^', markersize=7, color='k')

        ax1.plot(signals.loc[signals.orders == -1.0].index,
                 series[signals.orders == -1.0],
                 'v', markersize=7, color='k')

        plt.legend(["Price", "Highs", "Lows", "Average", "Buy", "Sell"])
        plt.title("Turtle Trading Strategy")

        plt.show()
