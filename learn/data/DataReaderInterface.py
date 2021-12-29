import pandas as pd

class DataReaderInterface:

    # def download_data(self, symbol, start, end) -> pd.DataFrame:
    #     """Load ticker learn"""
    #     pass

    def download_data(self, symbol, start, end, freq) -> pd.DataFrame:
        """Load ticker learn"""
        pass