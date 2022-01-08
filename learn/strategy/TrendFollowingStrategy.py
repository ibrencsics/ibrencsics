from learn.signal.Apo import Apo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class TrendFollowingStrategy:
    # Constants that define strategy behavior/thresholds
    APO_VALUE_FOR_BUY_ENTRY = 10  # APO trading signal value above which to enter buy-orders/long-position
    APO_VALUE_FOR_SELL_ENTRY = -10  # APO trading signal value below which to enter sell-orders/short-position
    MIN_PRICE_MOVE_FROM_LAST_TRADE = 10  # Minimum price change since last trade before considering trading again, this is to prevent over-trading at/around same prices
    NUM_SHARES_PER_TRADE = 10  # Number of shares to buy/sell on every trade
    MIN_PROFIT_TO_CLOSE = 10 * NUM_SHARES_PER_TRADE  # Minimum Open/Unrealized profit at which to close positions and lock profits
    SMA_NUM_PERIODS = 20

    def __init__(self):
        self.apo = Apo()

    def execute(self, close):

        # without volatility adjustment
        ema_fast, ema_slow, apo_series, = self.apo.calculate(close, 10, 40, 2)
        stdev_factor_series = np.ones(len(close))

        # with volatility adjustment
        # ema_fast, ema_slow, apo_series, stdev_factor_series = self.apo.calculateWithStdev(close, 10, 40, 2, self.SMA_NUM_PERIODS)

        # Variables for Trading Strategy trade, position & pnl management:
        orders = []  # Container for tracking buy/sell order, +1 for buy order, -1 for sell order, 0 for no-action
        positions = []  # Container for tracking positions, +ve for long positions, -ve for short positions, 0 for flat/no position
        pnls = []  # Container for tracking total_pnls, this is the sum of closed_pnl i.e. pnls already locked in and open_pnl i.e. pnls for open-position marked to market price

        last_buy_price = 0  # Price at which last buy trade was made, used to prevent over-trading at/around the same price
        last_sell_price = 0  # Price at which last sell trade was made, used to prevent over-trading at/around the same price
        position = 0  # Current position of the trading strategy
        buy_sum_price_qty = 0  # Summation of products of buy_trade_price and buy_trade_qty for every buy Trade made since last time being flat
        buy_sum_qty = 0  # Summation of buy_trade_qty for every buy Trade made since last time being flat
        sell_sum_price_qty = 0  # Summation of products of sell_trade_price and sell_trade_qty for every sell Trade made since last time being flat
        sell_sum_qty = 0  # Summation of sell_trade_qty for every sell Trade made since last time being flat
        open_pnl = 0  # Open/Unrealized PnL marked to market
        closed_pnl = 0  # Closed/Realized PnL so far

        for i in range(len(close)):
            close_price = close[i]
            apo = apo_series[i]
            stdev_factor = stdev_factor_series[i]

            # This section checks trading signal against trading parameters/thresholds and positions, to trade.

            # We will perform a sell trade at close_price if the following conditions are met:
            # 1. The APO trading signal value is below Sell-Entry threshold and the difference between last trade-price and current-price is different enough.
            # 2. We are long( +ve position ) and either APO trading signal value is at or below 0 or current position is profitable enough to lock profit.
            if ((apo < self.APO_VALUE_FOR_SELL_ENTRY/stdev_factor and abs(
                    close_price - last_sell_price) > self.MIN_PRICE_MOVE_FROM_LAST_TRADE*stdev_factor)  # APO above sell entry threshold, we should sell
                    or
                    (position > 0 and (
                            apo <= 0 or open_pnl > self.MIN_PROFIT_TO_CLOSE/stdev_factor))):  # long from +ve APO and APO has gone negative or position is profitable, sell to close position
                orders.append(-1)  # mark the sell trade
                last_sell_price = close_price
                position -= self.NUM_SHARES_PER_TRADE  # reduce position by the size of this trade
                sell_sum_price_qty += (close_price * self.NUM_SHARES_PER_TRADE)  # update vwap sell-price
                sell_sum_qty += self.NUM_SHARES_PER_TRADE
                print("Sell ", self.NUM_SHARES_PER_TRADE, " @ ", close_price, "Position: ", position)

            # We will perform a buy trade at close_price if the following conditions are met:
            # 1. The APO trading signal value is above Buy-Entry threshold and the difference between last trade-price and current-price is different enough.
            # 2. We are short( -ve position ) and either APO trading signal value is at or above 0 or current position is profitable enough to lock profit.
            elif ((apo > self.APO_VALUE_FOR_BUY_ENTRY/stdev_factor and abs(
                    close_price - last_buy_price) > self.MIN_PRICE_MOVE_FROM_LAST_TRADE*stdev_factor)  # APO above buy entry threshold, we should buy
                  or
                  (position < 0 and (
                          apo >= 0 or open_pnl > self.MIN_PROFIT_TO_CLOSE/stdev_factor))):  # short from -ve APO and APO has gone positive or position is profitable, buy to close position
                orders.append(+1)  # mark the buy trade
                last_buy_price = close_price
                position += self.NUM_SHARES_PER_TRADE  # increase position by the size of this trade
                buy_sum_price_qty += (close_price * self.NUM_SHARES_PER_TRADE)  # update the vwap buy-price
                buy_sum_qty += self.NUM_SHARES_PER_TRADE
                print("Buy ", self.NUM_SHARES_PER_TRADE, " @ ", close_price, "Position: ", position)
            else:
                # No trade since none of the conditions were met to buy or sell
                orders.append(0)

            positions.append(position)

            # This section updates Open/Unrealized & Closed/Realized positions
            open_pnl = 0
            if position > 0:
                if sell_sum_qty > 0:  # long position and some sell trades have been made against it, close that amount based on how much was sold against this long position
                    open_pnl = abs(sell_sum_qty) * (sell_sum_price_qty / sell_sum_qty - buy_sum_price_qty / buy_sum_qty)
                # mark the remaining position to market i.e. pnl would be what it would be if we closed at current price
                open_pnl += abs(sell_sum_qty - position) * (close_price - buy_sum_price_qty / buy_sum_qty)
            elif position < 0:
                if buy_sum_qty > 0:  # short position and some buy trades have been made against it, close that amount based on how much was bought against this short position
                    open_pnl = abs(buy_sum_qty) * (sell_sum_price_qty / sell_sum_qty - buy_sum_price_qty / buy_sum_qty)
                # mark the remaining position to market i.e. pnl would be what it would be if we closed at current price
                open_pnl += abs(buy_sum_qty - position) * (sell_sum_price_qty / sell_sum_qty - close_price)
            else:
                # flat, so update closed_pnl and reset tracking variables for positions & pnls
                closed_pnl += (sell_sum_price_qty - buy_sum_price_qty)
                buy_sum_price_qty = 0
                buy_sum_qty = 0
                sell_sum_price_qty = 0
                sell_sum_qty = 0
                last_buy_price = 0
                last_sell_price = 0

            print("OpenPnL: ", open_pnl, " ClosedPnL: ", closed_pnl, " TotalPnL: ", (open_pnl + closed_pnl))
            pnls.append(closed_pnl + open_pnl)


        # This section prepares the dataframe from the trading strategy results and visualizes the results
        data = close.to_frame()
        data = data.assign(ClosePrice=pd.Series(close, index=data.index))
        data = data.assign(Fast10DayEMA=pd.Series(ema_fast, index=data.index))
        data = data.assign(Slow40DayEMA=pd.Series(ema_slow, index=data.index))
        data = data.assign(APO=pd.Series(apo_series, index=data.index))
        data = data.assign(Trades=pd.Series(orders, index=data.index))
        data = data.assign(Position=pd.Series(positions, index=data.index))
        data = data.assign(Pnl=pd.Series(pnls, index=data.index))

        import matplotlib.pyplot as plt

        data['ClosePrice'].plot(color='blue', lw=3., legend=True)
        data['Fast10DayEMA'].plot(color='y', lw=1., legend=True)
        data['Slow40DayEMA'].plot(color='m', lw=1., legend=True)
        plt.plot(data.loc[data.Trades == 1].index, data.ClosePrice[data.Trades == 1], color='r', lw=0, marker='^',
                 markersize=7, label='buy')
        plt.plot(data.loc[data.Trades == -1].index, data.ClosePrice[data.Trades == -1], color='g', lw=0, marker='v',
                 markersize=7, label='sell')
        plt.legend()
        self.show_fullscreen()

        data['APO'].plot(color='k', lw=3., legend=True)
        plt.plot(data.loc[data.Trades == 1].index, data.APO[data.Trades == 1], color='r', lw=0, marker='^',
                 markersize=7, label='buy')
        plt.plot(data.loc[data.Trades == -1].index, data.APO[data.Trades == -1], color='g', lw=0, marker='v',
                 markersize=7, label='sell')
        plt.axhline(y=0, lw=0.5, color='k')
        for i in range(self.APO_VALUE_FOR_BUY_ENTRY, self.APO_VALUE_FOR_BUY_ENTRY * 5, self.APO_VALUE_FOR_BUY_ENTRY):
            plt.axhline(y=i, lw=0.5, color='r')
        for i in range(self.APO_VALUE_FOR_SELL_ENTRY, self.APO_VALUE_FOR_SELL_ENTRY * 5, self.APO_VALUE_FOR_SELL_ENTRY):
            plt.axhline(y=i, lw=0.5, color='g')
        plt.legend()
        self.show_fullscreen()

        data['Position'].plot(color='k', lw=1., legend=True)
        plt.plot(data.loc[data.Position == 0].index, data.Position[data.Position == 0], color='k', lw=0, marker='.',
                 label='flat')
        plt.plot(data.loc[data.Position > 0].index, data.Position[data.Position > 0], color='r', lw=0, marker='+',
                 label='long')
        plt.plot(data.loc[data.Position < 0].index, data.Position[data.Position < 0], color='g', lw=0, marker='_',
                 label='short')
        plt.axhline(y=0, lw=0.5, color='k')
        for i in range(self.NUM_SHARES_PER_TRADE, self.NUM_SHARES_PER_TRADE * 25, self.NUM_SHARES_PER_TRADE * 5):
            plt.axhline(y=i, lw=0.5, color='r')
        for i in range(-self.NUM_SHARES_PER_TRADE, -self.NUM_SHARES_PER_TRADE * 25, -self.NUM_SHARES_PER_TRADE * 5):
            plt.axhline(y=i, lw=0.5, color='g')
        plt.legend()
        self.show_fullscreen()

        data['Pnl'].plot(color='k', lw=1., legend=True)
        plt.plot(data.loc[data.Pnl > 0].index, data.Pnl[data.Pnl > 0], color='g', lw=0, marker='.')
        plt.plot(data.loc[data.Pnl < 0].index, data.Pnl[data.Pnl < 0], color='r', lw=0, marker='.')
        plt.legend()
        self.show_fullscreen()

        # data.to_csv("basic_trend_following.csv", sep=",")

    def show_fullscreen(self):
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()