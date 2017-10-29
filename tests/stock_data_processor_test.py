from unittest import TestCase, main, skip
from ..finance.stock_data_processor import StockDataProcessor


class StockDataProcessorTest(TestCase):

    def test_stock_data_processor_wrong_name(self):
        start, end = "2016-02-02", "2017-02-02"
        self.assertRaises(RuntimeError, StockDataProcessor, None, start, end)
        self.assertRaises(RuntimeError, StockDataProcessor, 1, start, end)
        self.assertRaises(RuntimeError, StockDataProcessor, [], start, end)
        self.assertRaises(RuntimeError, StockDataProcessor, (), start, end)
        self.assertRaises(RuntimeError, StockDataProcessor, {}, start, end)

    def test_stock_data_processor_wrong_date(self):
        name = "BIDU"
        start, end = "2016-02-02", "2017-02-02"
        self.assertRaises(RuntimeError, StockDataProcessor, name, end, start)
        start_wrong_format = "02-02-2016"
        self.assertRaises(RuntimeError, StockDataProcessor, name, start_wrong_format, end)
        end_wrong_format = "2016-31-12"
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end_wrong_format)

    def test_stock_data_processor_wrong_data_source(self):
        name = "BIDU"
        start, end = "2016-02-02", "2017-02-02"
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end, None)
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end, 2)
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end, {})
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end, [])
        self.assertRaises(RuntimeError, StockDataProcessor, name, start, end, ())

        sdp = StockDataProcessor(name, start, end, 'test')
        self.assertRaises(RuntimeError, sdp.get_stock_data)

    # NOTE: This test is not mocked. Therefore, it may be broken because of external services or
    # lack of internet connection
    # TODO: Fix this test
    @skip("Need to do stub for such a test")
    def test_stock_data_processor_proper_parameters(self):
        name = "BIDU"
        start, end = "2017-02-01", "2017-02-01"
        sdp = StockDataProcessor(name, start, end)

        import datetime as dt
        import pandas as pd
        data = {'Close': {pd.Timestamp(dt.datetime(2017, 2, 1)): 173.81999999999999},
                'High': {pd.Timestamp(dt.datetime(2017, 2, 1)): 176.72999999999999},
                'Low': {pd.Timestamp(dt.datetime(2017, 2, 1)): 172.55000000000001},
                'Open': {pd.Timestamp(dt.datetime(2017, 2, 1)): 176.72999999999999},
                'Volume': {pd.Timestamp(dt.datetime(2017, 2, 1)): 1216389}}

        self.assertEqual(data, sdp.get_stock_data().to_dict())

        start, end = "2017-02-02", "2017-02-02"
        sdp = StockDataProcessor(name, start, end)
        self.assertNotEqual(data, sdp.get_stock_data().to_dict())


if __name__ == '__main__':
    main()
