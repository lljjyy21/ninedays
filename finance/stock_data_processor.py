import datetime as dt
import pandas_datareader.data as web


# TODO: Add documentation
class StockDataProcessor:
    def __init__(self, name, start, end, data_source='google'):
        if name is None or not isinstance(name, basestring) or \
           data_source is None or not isinstance(data_source, basestring):
            raise RuntimeError
        else:
            self.name = name.upper()
            self.data_source = data_source
        try:
            self.start = dt.datetime.strptime(start, '%Y-%m-%d')
            self.end = dt.datetime.strptime(end, '%Y-%m-%d')
            if self.start > self.end:
                raise Exception
        except Exception as e:
            raise RuntimeError
        self.stock_data = None

    def get_stock_data(self):
        if self.stock_data is None:
            try:
                self.stock_data = web.DataReader('NASDAQ:' + self.name, self.data_source, self.start, self.end)
            except NotImplementedError as e:
                raise RuntimeError
        data = self.stock_data[:]

        return data
