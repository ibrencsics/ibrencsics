import matplotlib.pyplot as plt
import pandas as pd
from data.visualize.VisualizerInterface import VisualizerInterface

class PandasPlotVisualizer(VisualizerInterface):

    colors = ['g', 'b', 'r', 'c', 'm']

    def plot(self, df, symbol):
        df_plot = self.get_close_df(df)

        # option 1
        # pd.options.plotting.backend = "plotly"
        # fig = df_plot.plot(title=symbol + ' time series')
        # fig.show()

        # option 2
        fig, axes = plt.subplots(figsize=(24, 20), sharex=True)
        df_plot.plot()
        plt.show()

    def plot_series(self, series, symbol):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel=symbol + ' price in $')
        for i in range(len(series)):
            series[i].plot(ax=ax1, color=self.colors[i], lw=2., legend=True)

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        # manager.full_screen_toggle()
        plt.show()

    def plot_series_subplots(self, symbol, series1, series2=None, series3=None):
        fig = plt.figure()

        hundred = 100
        if series2 is not None:
            hundred += 100
        if series3 is not None:
            hundred += 100

        ax1 = fig.add_subplot(hundred + 11, ylabel=symbol + ' price in $')
        for i in range(len(series1)):
            series1[i].plot(ax=ax1, color=self.colors[i], lw=2., legend=True)

        if series2 is not None:
            ax2 = fig.add_subplot(hundred + 12, ylabel='')
            for i in range(len(series2)):
                series2[i].plot(ax=ax2, color=self.colors[i], lw=2., legend=True)

        if series3 is not None:
            ax3 = fig.add_subplot(hundred + 13, ylabel='')
            for i in range(len(series3)):
                series3[i].plot(ax=ax3, color=self.colors[i], lw=2., legend=True)

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()

    def plot_series_histogram(self, series1, series2, series3, symbol):
        fig = plt.figure()

        ax1 = fig.add_subplot(311, ylabel=symbol + ' price in $')
        for i in range(len(series1)):
            series1[i].plot(ax=ax1, color=self.colors[i], lw=2., legend=True)

        ax2 = fig.add_subplot(312, ylabel='MACD')
        for i in range(len(series2)):
            series2[i].plot(ax=ax2, color=self.colors[i], lw=2., legend=True)

        ax3 = fig.add_subplot(313, ylabel='MACD')
        for i in range(len(series3)):
            series3[i].plot(ax=ax3, color='r', kind='bar', legend=True, use_index=False)

        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()

    def test(self, series):
        series.boxplot(column='monthly_return', by='month')
        ax = plt.gca()
        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', \
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax.set_xticklabels(labels)
        ax.set_ylabel('GOOG return')
        plt.tick_params(axis='both', which='major', labelsize=7)
        plt.title("GOOG Montly return 2001-2018")
        plt.suptitle("")
        plt.show()
