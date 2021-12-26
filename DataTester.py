from data.CachingDataProvider import CachingDataProvider
from data.FinnhubReader import FinnhubReader
from data.IntrinioReader import IntrinioReader
from data.PandasDataReader import PandasDataReader
from data.QuandlReader import QuandlReader
from data.YFinanceReader import YFinanceReader

from data.visualize.PandasPlotVisualizer import PandasPlotVisualizer

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

df = provider.download_data(finnReader, 'AAPL', '2021-12-23T09:30:00-05:00', '2021-12-23T16:00:00-05:00', '1m')
pandasPlotVisualizer.plot(df, 'AAPL')