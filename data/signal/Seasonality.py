import pandas as pd
from statsmodels.tsa.stattools import adfuller

from data.visualize.PandasPlotVisualizer import PandasPlotVisualizer

class Seasonality:

    def __init__(self):
        self.visualizer = PandasPlotVisualizer()

    def test(self, series):
        monthly_return, monthly_return_list = self.get_monthly_return(series)
        self.visualize_returns(series, monthly_return, monthly_return_list)

        self.test_stationarity(monthly_return[1:])
        self.test_stationarity(series)

        self.visualizer.plot_test1(monthly_return)
        self.visualizer.plot_arima(monthly_return)

        return monthly_return_list

    def get_monthly_return(self, series):
        monthly_return = series.pct_change()\
            .groupby([series.index.year, series.index.month])\
            .mean()

        monthly_return_list = []
        for i in range(len(monthly_return)):
            monthly_return_list.append(
                {
                    'month': monthly_return.index[i][1],
                    'monthly_return': monthly_return.values[i]
                }
            )
        monthly_return_list = pd.DataFrame(monthly_return_list, columns=('month', 'monthly_return'))

        return monthly_return, monthly_return_list

    def visualize_returns(self, series, monthly_return, monthly_return_list):
        self.visualizer.monthly_return(monthly_return_list)
        self.visualizer.plot_series([monthly_return], 'GOOG')

        self.visualizer.plot_rolling_statistics(
            monthly_return[1:],
            'GOOG prices rolling mean and standard deviation',
            'Monthly return')

        self.visualizer.plot_rolling_statistics(
            series,
            'GOOG prices rolling mean and standard deviation',
            'Daily prices',
            365)

        self.visualizer.plot_rolling_statistics(
            series - series.rolling(365).mean(),
            'GOOG prices without trend',
            'Daily prices',
            365)

    def test_stationarity(self, timeseries):
        print('Results of Dickey-Fuller Test:')
        dftest = adfuller(timeseries[1:], autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        print(dfoutput)
