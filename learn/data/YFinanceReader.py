import pandas as pd
import yfinance as yf
from learn.data.DataReaderInterface import DataReaderInterface

column_dist = {
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Adj Close': 'adj_close',
    'Volume': 'volume'
}

class YFinanceReader(DataReaderInterface):

    def download_data(self, symbol, start, end, freq='1d') -> pd.DataFrame:
        df = yf.download(tickers=symbol, start=start, end=end, interval=freq, progress=False)
        df = df.rename(columns=column_dist)
        return df

# https://algotrading101.com/learn/yfinance-guide/

# yfReader.download_data('AAPL', '2021-12-23', '2021-12-24', '1m')
# this returns learn starting from 9:30 EST


# period: learn period to download (either use period parameter or use start and end) Valid periods are:
# “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
# interval: learn interval (1m learn is only for available for last 7 days, and learn interval <1d for the last 60 days) Valid intervals are:
# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
# start: If not using period – in the format (yyyy-mm-dd) or datetime.
# end: If not using period – in the format (yyyy-mm-dd) or datetime.
# prepost: Include Pre and Post regular market learn in results? (Default is False)- no need usually to change this from False
# auto_adjust: Adjust all OHLC (Open/High/Low/Close prices) automatically? (Default is True)- just leave this always as true and don’t worry about it
# actions: Download stock dividends and stock splits events? (Default is True)