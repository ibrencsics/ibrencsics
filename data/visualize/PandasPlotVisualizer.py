import matplotlib.pyplot as plt
import pandas as pd
from data.visualize.VisualizerInterface import VisualizerInterface

class PandasPlotVisualizer(VisualizerInterface):

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

