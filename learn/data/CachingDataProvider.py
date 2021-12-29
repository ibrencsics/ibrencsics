import pandas as pd

class CachingDataProvider:

    def get_filename(self, symbol, data_reader_name, start_date, end_date, frequency):
        return 'learn/download/%s_%s_%s_%s_%s.pkl' % (symbol, data_reader_name, start_date, end_date, frequency)

    def download_data(self, data_reader, symbol, start_date, end_date, frequency):
        file_name = self.get_filename(symbol, type(data_reader).__name__, start_date, end_date, frequency)

        try:
            data = pd.read_pickle(file_name)
            print('File learn found...reading ticker learn')
        except FileNotFoundError:
            print('File not found...downloading the ticker learn')
            data = data_reader.download_data(symbol, start_date, end_date, frequency)
            data.to_pickle(file_name)

        return data


