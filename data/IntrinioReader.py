import intrinio_sdk
import pandas as pd
from data.DataReaderInterface import DataReaderInterface

freq_dist = {
    '1mo': 'monthly',
    '1wk': 'weekly',
    '1d': 'daily'
}

class IntrinioReader(DataReaderInterface):

    def download_data(self, symbol, start, end, freq) -> pd.DataFrame:
        intrinio_sdk.ApiClient().configuration.api_key['api_key'] = '{OmZhN2M0NGZmZTk2MmM1YTZjYjkyMDI0NTI3OTc4MjAw}'
        security_api = intrinio_sdk.SecurityApi()
        r = security_api.get_security_stock_prices(
            identifier=symbol,
            start_date=start,
            end_date=end,
            frequency=freq_dist.get(freq),
            page_size=10000)
        response_list = [x.to_dict() for x in r.stock_prices]
        df_intrinio = pd.DataFrame(response_list).sort_values('date')
        df_intrinio.set_index('date', inplace=True)
        return df_intrinio

# colums:
# 'intraperiod', 'frequency', 'open', 'high', 'low', 'close', 'volume',
# 'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume', 'factor',
# 'split_ratio', 'dividend', 'change', 'percent_change',
# 'fifty_two_week_high', 'fifty_two_week_low'