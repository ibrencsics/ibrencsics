import pandas as pd
import pandas_datareader.data as web
from learn.data.DataReaderInterface import DataReaderInterface

class PandasDataReader(DataReaderInterface):

    def download_data(self, symbol, start, end, freq=None) -> pd.DataFrame:
        df = web.DataReader(name=symbol, data_source='yahoo', start=start, end=end)
        return df

# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html