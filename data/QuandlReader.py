import quandl
import pandas as pd
from data.DataReaderInterface import DataReaderInterface

QUANDL_KEY = 'r2yvZufsxoZz7DyJS8ft'
quandl.ApiConfig.api_key = QUANDL_KEY

# Works only until 2018
class QuandlReader(DataReaderInterface):

    def download_data(self, symbol, start, end) -> pd.DataFrame:
        df = quandl.get(dataset='WIKI/' + symbol, start_date=start, end_date=end)
        return df