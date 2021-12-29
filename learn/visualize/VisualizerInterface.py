import datetime

class VisualizerInterface:

    def plot(self, df, symbol):
        pass

    def plot_series(self, series, symbol):
        pass

    def get_close_df(self, df):
        df_plot = df.close
        df_plot.index = df_plot.index.map(self.format_date)
        return df_plot

    def format_date(self, iso):
        return datetime.datetime.fromisoformat(iso).time()