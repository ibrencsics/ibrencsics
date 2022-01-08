import numpy as np
from statsmodels.tsa.stattools import coint
import seaborn
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

class PairsCorrelation:

    def find_cointegrated_pairs(self, data):
        n = data.shape[1]
        pvalue_matrix = np.ones((n, n))
        keys = data.keys()
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                result = coint(data[keys[i]], data[keys[j]])
                pvalue_matrix[i, j] = result[1]
                if result[1] < 0.02:
                    pairs.append((keys[i], keys[j]))
        return pvalue_matrix, pairs

    def show_fullscreen(self):
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()

    def test(self, data, symbol1, symbol2):
        margin = 1.2

        symbol1_prices = data['Adj Close'][symbol1]
        symbol1_prices.name = symbol1
        symbol2_prices = data['Adj Close'][symbol2]
        symbol2_prices.name = symbol2
        plt.title('symbol1' + 'and ' + symbol2 + ' prices')
        symbol1_prices.plot()
        symbol2_prices.plot()
        plt.legend()
        self.show_fullscreen()

        score, pvalue, _ = coint(symbol1_prices, symbol2_prices)
        print(pvalue)

        ratios = symbol1_prices / symbol2_prices
        plt.title("Ration between Symbol 1 and Symbol 2 price")
        ratios.plot()
        self.show_fullscreen()

        self.zscore(ratios).plot()
        plt.title("Z-score evolution")
        plt.axhline(self.zscore(ratios).mean(), color="black")
        plt.axhline(margin, color="red")
        plt.axhline(-margin, color="green")
        self.show_fullscreen()

        ratios.plot()
        buy = ratios.copy()
        sell = ratios.copy()
        buy[self.zscore(ratios) > -margin] = 0
        sell[self.zscore(ratios) < margin] = 0
        buy.plot(color="g", linestyle="None", marker="^")
        sell.plot(color="r", linestyle="None", marker="v")
        x1, x2, y1, y2 = plt.axis()
        plt.axis((x1, x2, ratios.min(), ratios.max()))
        plt.legend(["Ratio", "Buy Signal", "Sell Signal"])
        self.show_fullscreen()

        # symbol1, symbol2 buy
        s1_min = symbol1_prices.min()
        s1_max = symbol1_prices.max()
        s2_min = symbol2_prices.min()
        s2_max = symbol2_prices.max()
        scale_min = np.minimum(s1_min, s2_min)
        scale_max = np.maximum(s1_max, s2_max)

        symbol1_buy = symbol1_prices.copy()
        symbol1_sell = symbol1_prices.copy()
        symbol2_buy = symbol2_prices.copy()
        symbol2_sell = symbol2_prices.copy()

        symbol1_prices.plot()
        symbol1_buy[self.zscore(ratios) > -margin] = 0
        symbol1_sell[self.zscore(ratios) < margin] = 0
        symbol1_buy.plot(color="g", linestyle="None", marker="^")
        symbol1_sell.plot(color="r", linestyle="None", marker="v")

        symbol2_prices.plot()
        symbol2_buy[self.zscore(ratios) < margin] = 0
        symbol2_sell[self.zscore(ratios) > -margin] = 0
        symbol2_buy.plot(color="g", linestyle="None", marker="^")
        symbol2_sell.plot(color="r", linestyle="None", marker="v")

        x1, x2, y1, y2 = plt.axis()
        plt.axis((x1, x2, scale_min, scale_max))
        plt.legend(["Symbol1", "Buy Signal", "Sell Signal", "Symbol2"])
        self.show_fullscreen()

        #
        pair_correlation_trading_strategy = pd.DataFrame(index=symbol1_prices.index)
        pair_correlation_trading_strategy['symbol1_price'] = symbol1_prices
        pair_correlation_trading_strategy['symbol1_buy'] = np.zeros(len(symbol1_prices))
        pair_correlation_trading_strategy['symbol1_sell'] = np.zeros(len(symbol1_prices))
        pair_correlation_trading_strategy['symbol2_buy'] = np.zeros(len(symbol1_prices))
        pair_correlation_trading_strategy['symbol2_sell'] = np.zeros(len(symbol1_prices))

        position = 0
        for i in range(len(symbol1_prices)):
            s1price = symbol1_prices[i]
            s2price = symbol2_prices[i]
            if not position and symbol1_buy[i] != 0:
                pair_correlation_trading_strategy['symbol1_buy'][i] = s1price
                pair_correlation_trading_strategy['symbol2_sell'][i] = s2price
                position = 1
            elif not position and symbol1_sell[i] != 0:
                pair_correlation_trading_strategy['symbol1_sell'][i] = s1price
                pair_correlation_trading_strategy['symbol2_buy'][i] = s2price
                position = -1
            elif position == -1 and (symbol1_sell[i] == 0 or i == len(symbol1_prices) - 1):
                pair_correlation_trading_strategy['symbol1_buy'][i] = s1price
                pair_correlation_trading_strategy['symbol2_sell'][i] = s2price
                position = 0
            elif position == 1 and (symbol1_buy[i] == 0 or i == len(symbol1_prices) - 1):
                pair_correlation_trading_strategy['symbol1_sell'][i] = s1price
                pair_correlation_trading_strategy['symbol2_buy'][i] = s2price
                position = 0

        symbol1_prices.plot()
        pair_correlation_trading_strategy['symbol1_buy'].plot(color="g", linestyle="None", marker="^")
        pair_correlation_trading_strategy['symbol1_sell'].plot(color="r", linestyle="None", marker="v")
        symbol2_prices.plot()
        pair_correlation_trading_strategy['symbol2_buy'].plot(color="g", linestyle="None", marker="^")
        pair_correlation_trading_strategy['symbol2_sell'].plot(color="r", linestyle="None", marker="v")
        x1, x2, y1, y2 = plt.axis()
        plt.axis((x1, x2, scale_min, scale_max))
        plt.legend(["Symbol1", "Buy Signal", "Sell Signal", "Symbol2"])
        self.show_fullscreen()

        # P&L
        pair_correlation_trading_strategy['symbol1_position'] = \
            pair_correlation_trading_strategy['symbol1_buy'] - pair_correlation_trading_strategy['symbol1_sell']

        pair_correlation_trading_strategy['symbol2_position'] = \
            pair_correlation_trading_strategy['symbol2_buy'] - pair_correlation_trading_strategy['symbol2_sell']

        pair_correlation_trading_strategy['symbol1_position'].cumsum().plot()
        pair_correlation_trading_strategy['symbol2_position'].cumsum().plot()

        pair_correlation_trading_strategy['total_position'] = \
            pair_correlation_trading_strategy['symbol1_position'] + pair_correlation_trading_strategy[
                'symbol2_position']
        pair_correlation_trading_strategy['total_position'].cumsum().plot()
        plt.title("Symbol 1 and Symbol 2 positions")
        plt.legend()
        self.show_fullscreen()

    def zscore(self, series):
        return (series - series.mean()) / np.std(series)

    def visualize(self, symbolsIds, pvalues):
        seaborn.heatmap(pvalues, xticklabels=symbolsIds,
                        yticklabels=symbolsIds, cmap='RdYlGn_r',
                        mask=(pvalues >= 0.98))
        plt.show()
