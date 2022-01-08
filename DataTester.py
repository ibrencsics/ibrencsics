from learn.data.CachingDataProvider import CachingDataProvider
from learn.data.FinnhubReader import FinnhubReader
from learn.data.IntrinioReader import IntrinioReader
from learn.data.PandasDataReader import PandasDataReader
from learn.data.QuandlReader import QuandlReader
from learn.data.YFinanceReader import YFinanceReader
from learn.signal.Apo import Apo
from learn.signal.Bbands import Bbands
from learn.signal.Macd import Macd

from learn.visualize.PandasPlotVisualizer import PandasPlotVisualizer

yfReader = YFinanceReader()
qReader = QuandlReader()
iReader = IntrinioReader()
finnReader = FinnhubReader()
pandasReader = PandasDataReader()

provider = CachingDataProvider()

pandasPlotVisualizer = PandasPlotVisualizer()

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”



# df = yfReader.download_data('AAPL', '2021-12-23', '2021-12-24', '1m')
# print(df.head())

# df = qReader.download_data('AAPL', '2019-01-01', '2019-02-01')
# print(df.head())

# df = iReader.download_data('AAPL', '2019-01-01', '2019-02-01', '1d')
# print(df.head())

# df = finnReader.download_data('AAPL', '2021-12-23', '2021-12-24', '30m')
# df = finnReader.download_data('AAPL', '2021-12-23T09:30:00-05:00', '2021-12-23T16:00:00-05:00', '1m')
# print(df.head())

# df = pandasReader.download_data('AAPL', '2019-01-01', '2019-02-01')
# print(df.head())



# df = provider.download_data(yfReader, 'AAPL', '2021-12-23', '2021-12-24', '1m')
# print(df.head())

# df = provider.download_data(qReader, 'AAPL', '2000-01-01', '2000-02-01')
# print(df.head())

# df = provider.download_data(iReader, 'AAPL', '2021-01-01', '2021-12-24', '1d')
# print(df.head())

# df = provider.download_data(finnReader, 'AAPL', '2021-12-23T09:30:00-05:00', '2021-12-23T16:00:00-05:00', '1m')
# pandasPlotVisualizer.plot(df, 'AAPL')


# ticker = 'GOOG'
# df = provider.download_data(yfReader, ticker, '2014-01-01', '2018-01-01', '1d')
# df_tail = df.tail(620)
# close = df_tail.close

# sma = Sma()
# sma50 = sma.calculate(close, 50)
# sma200 = sma.calculate(close, 200)
# pandasPlotVisualizer.plot_series([close, sma50, sma200], ticker)

# ema = Ema()
# ema50 = ema.calculate(close, 50, 2)
# ema200 = ema.calculate(close, 200, 2)
# pandasPlotVisualizer.plot_series([close, ema50, ema200], ticker)

# apo = Apo()
# ema_fast, ema_slow, apo_val = apo.calculate(close, 10, 40, 2)
# pandasPlotVisualizer.plot_series_subplots(ticker, [close, ema_fast, ema_slow], [apo_val])

# macd = Macd()
# ema_fast, ema_slow, apo, macd_signal, macd_histogram = macd.calculate(close, 10, 40, 20, 2)
# pandasPlotVisualizer.plot_series_histogram([close, ema_fast, ema_slow], [apo, macd_signal], [macd_histogram], ticker)

# bbands = Bbands()
# sma, lower, upper = bbands.calculate(close, 20, 2)
# pandasPlotVisualizer.plot_series([close, sma, lower, upper], ticker)

# rsi = Rsi()
# gain_series, loss_series, rsi_series = rsi.calculate(close, 20)
# pandasPlotVisualizer.plot_series_subplots(ticker, [close], [gain_series, loss_series], [rsi_series])

# stdev = Stdev()
# stdev_series = stdev.calculate(close, 20)
# pandasPlotVisualizer.plot_series_subplots(ticker, [close], [stdev_series])
# stdev_series = stdev.calculate_manual(close, 20)
# pandasPlotVisualizer.plot_series_subplots(ticker, [close], [stdev_series])


# mom = Mom()
# mom_series = mom.calculate(close, 20)
# pandasPlotVisualizer.plot_series_subplots(ticker, [close], [mom_series])


# df = provider.download_data(yfReader, ticker, '2001-01-01', '2018-01-01', '1d')
# adj_close = df.adj_close
# seasonality = Seasonality()
# seasonality.test(adj_close)
