import pandas as pd
import matplotlib.pyplot as plt

class NaiveMomentumStrategy:

    def calculate(self, series):
        signals = self.naive_momentum_trading(series, 5)
        self.visualize(series, signals)

    def naive_momentum_trading(self, series, nb_conseq_days):
        signals = pd.DataFrame(index=series.index)
        signals['orders'] = 0
        cons_day = 0
        prior_price = 0
        init = True
        for k in range(len(series)):
            price = series[k]
            if init:
                prior_price = price
                init = False
            elif price > prior_price:
                if cons_day < 0:
                    cons_day = 0
                cons_day += 1
            elif price < prior_price:
                if cons_day > 0:
                    cons_day = 0
                cons_day -= 1
            if cons_day == nb_conseq_days:
                signals['orders'][k] = 1
            elif cons_day == -nb_conseq_days:
                signals['orders'][k] = -1
            prior_price = price

        return signals

    def visualize(self, series, signals):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Google price in $')
        series.plot(ax=ax1, color='g', lw=.5)

        ax1.plot(signals.loc[signals.orders == 1.0].index,
                 series[signals.orders == 1],
                 '^', markersize=7, color='k')

        ax1.plot(signals.loc[signals.orders == -1.0].index,
                 series[signals.orders == -1],
                 'v', markersize=7, color='k')

        plt.legend(["Price", "Buy", "Sell"])
        plt.title("Naive Momentum Trading Strategy")

        plt.show()
