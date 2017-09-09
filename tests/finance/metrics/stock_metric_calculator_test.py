from unittest import TestCase, main, TestLoader, TextTestRunner
from finance.metrics.stock_metric_calculator import StockMetricCalculator
from finance.events.average_event import AverageEvent
from finance.stock_data_processor import StockDataProcessor


class StockMetricCalculatorTest(TestCase):

    # TODO: Potentially, make a mock of this call
    def setUp(self):
        name = "GOOG"
        start, end = "2017-01-03", "2017-01-06"
        sdp = StockDataProcessor(name, start, end)
        data = sdp.get_stock_data()

        open_price, close_price = data['Open'].values, data['Close'].values
        average_event = AverageEvent(open_price, close_price)
        self.metric = StockMetricCalculator(data, average_event)

    def test_stock_metric_calculator_chance_of_rise(self):
        self.assertEqual(50.0, self.metric.calculate_chance_of_rise())

    def test_stock_metric_calculator_average_rise_percent(self):
        self.assertEqual(1.37, self.metric.calculate_average_rise_percent())

    def test_stock_metric_calculator_average_continuous_days(self):
        self.assertAlmostEquals(100.0, self.metric.calculate_average_continuous_days())


if __name__ == '__main__':
    main()
