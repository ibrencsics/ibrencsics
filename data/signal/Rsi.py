'''
The Relative Strength Index (RSI) was published
 by J. Welles Wilder. The current price is normalized as a percentage
 between 0 and 100. The name of this oscillator is misleading because
 it does not compare the instrument relative to another instrument
 or set of instruments, but rather represents the current price relative
 to other recent pieces within the selected lookback window length.

 RSI = 100 - (100 / (1 + RS))

Where:
 RS = ratio of smoothed average of n-period gains divided by the
 absolute value of the smoothed average of n-period losses.
 '''

import statistics as stats
import pandas as pd

class Rsi:

    def calculate(self, series, time_period):
        gain_history = []  # history of gains over look back period (0 if no gain, magnitude of gain if gain)
        loss_history = []  # history of losses over look back period (0 if no loss, magnitude of loss if loss)
        avg_gain_values = []  # track avg gains for visualization purposes
        avg_loss_values = []  # track avg losses for visualization purposes
        rsi_values = []  # track computed RSI values
        last_price = 0  # current_price - last_price > 0 => gain. current_price - last_price < 0 => loss.

        for val in series:
            if last_price == 0:
                last_price = val

            gain_history.append(max(0, val - last_price))
            loss_history.append(max(0, last_price - val))
            last_price = val

            if len(gain_history) > time_period:  # maximum observations is equal to lookback period
                del (gain_history[0])
                del (loss_history[0])

            avg_gain = stats.mean(gain_history)  # average gain over lookback period
            avg_loss = stats.mean(loss_history)  # average loss over lookback period

            avg_gain_values.append(avg_gain)
            avg_loss_values.append(avg_loss)

            rs = 0
            if avg_loss > 0:  # to avoid division by 0, which is undefined
                rs = avg_gain / avg_loss

            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

        gain_series = pd.Series(data=avg_gain_values, index=series.index, name='gainOver' + str(time_period))
        loss_series = pd.Series(data=avg_loss_values, index=series.index, name='lossOver' + str(time_period))
        rsi_series = pd.Series(data=rsi_values, index=series.index, name='rsi' + str(time_period))

        return gain_series, loss_series, rsi_series
