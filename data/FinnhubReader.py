import finnhub
import pandas as pd
import dateutil.parser as dp
import datetime
import pytz

# Setup client
from data.DataReaderInterface import DataReaderInterface

freq_dist = {
    '3mo': 'M',
    '1mo': 'M',
    '1wk': 'W',
    '5d': 'W',
    '1d': 'D',
    '1h': '60',
    '30m': '30',
    '15m': '15',
    '5m': '5',
    '2m': '1',
    '1m': '1'
}

column_dist = {
    'o': 'open',
    'h': 'high',
    'l': 'low',
    'c': 'close',
    't': 'Date',
    'v': 'volume',
    's': 'status'
}

timezone = pytz.timezone('America/New_York')

finnhub_client = finnhub.Client(api_key="bua8bcf48v6q418ga8d0")

class FinnhubReader(DataReaderInterface):

    def download_data(self, symbol, start, end, freq='1d') -> pd.DataFrame:
        # Stock candles
        res = finnhub_client.stock_candles(symbol, freq_dist.get(freq), self.isoToUnix(start), self.isoToUnix(end))
        # print(res)
        df = pd.DataFrame(res)
        df.t = df.t.apply(self.unixToIso)
        df = df.rename(columns=column_dist)
        df = df.set_index('Date')
        return df

    def isoToUnix(self, iso_date) -> int:
        # https://docs.python.org/3/library/datetime.html
        return int(dp.parse(iso_date).timestamp())

    def unixToIso(self, unixDate) -> str:
        dt = datetime.datetime.fromtimestamp(unixDate)
        dt_est = dt.astimezone(timezone)
        return dt_est.isoformat(timespec='seconds')

# https://github.com/Finnhub-Stock-API/finnhub-python

# has to be called like this:
# finnReader.download_data('AAPL', '2021-12-23T09:30:00-05:00', '2021-12-23T16:00:00-05:00', '1m')