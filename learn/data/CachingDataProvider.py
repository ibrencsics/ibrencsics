import pandas as pd

class CachingDataProvider:

    def get_filename(self, symbol, data_reader_name, start_date, end_date, frequency):
        symbol_name = '-'.join(symbol) if isinstance(symbol, list) else symbol
        return 'learn/download/%s_%s_%s_%s_%s.pkl' % (symbol_name, data_reader_name, start_date, end_date, frequency)

    def download_data(self, data_reader, symbol, start_date, end_date, frequency):
        file_name = self.get_filename(symbol, type(data_reader).__name__, start_date, end_date, frequency)

        try:
            data = pd.read_pickle(file_name)
            print('File {} found...'.format(file_name))
        except FileNotFoundError:
            print('File not found...downloading to file {}'.format(file_name))
            data = data_reader.download_data(symbol, start_date, end_date, frequency)
            data.to_pickle(file_name)

        return data
