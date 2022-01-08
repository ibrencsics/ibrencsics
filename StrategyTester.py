from learn.data.CachingDataProvider import CachingDataProvider
from learn.data.PandasDataReader import PandasDataReader
from learn.data.YFinanceReader import YFinanceReader
from learn.strategy.MeanReversionStrategy import MeanReversionStrategy
from learn.strategy.DualMovingAverageStrategy import DualMovingAverageStrategy
from learn.strategy.NaiveMomentumStrategy import NaiveMomentumStrategy
from learn.strategy.PairsCorrelation import PairsCorrelation
from learn.strategy.TrendFollowingStrategy import TrendFollowingStrategy
from learn.strategy.TurtleStrategy import TurtleStrategy

yfReader = YFinanceReader()
pdReader = PandasDataReader()
provider = CachingDataProvider()

ticker = 'GOOG'
df = provider.download_data(yfReader, ticker, '2014-01-01', '2018-01-01', '1d')
close = df.close
adj_close = df.adj_close

# DualMovingAverageStrategy().calculate(adj_close)
# NaiveMomentumStrategy().calculate(adj_close)
# TurtleStrategy().calculate(adj_close)

# pairs_corr = PairsCorrelation()
# symbolsIds = ['SPY', 'AAPL', 'ADBE', 'LUV', 'MSFT', 'SKYW','QCOM', 'HPQ', 'JNPR', 'AMD', 'IBM']
# symbolsIds = ['AAPL', 'GOOG', 'FB', 'AMZN', 'MSFT']
# data = provider.download_data(pdReader, symbolsIds, '2015-01-01', '2022-01-01', '1d')
# pvalues, pairs = pairs_corr.find_cointegrated_pairs(data['Adj Close'])
# pairs_corr.visualize(symbolsIds, pvalues)
# pairs_corr.test(data, 'GOOG', 'AMZN')
# pairs_corr.test(data, 'MSFT', 'AAPL')

# mr = MeanReversionStrategy()
# mr.execute(close)

tf = TrendFollowingStrategy()
tf.execute(close)