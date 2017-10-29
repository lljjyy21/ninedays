from unittest import TestCase, main, skip
from ...finance.metrics.stock_metric_calculator import StockMetricCalculator
from ...finance.events.average_event import AverageEvent
from ...finance.events.moving_average_event import MovingAverageEvent
from ...finance.events.pass_resistance_line_event import PassResistanceLineEvent
from ...finance.events.small_movement_event import SmallMovementEvent
from ...finance.events.support_line_rebound_event import SupportLineReboundEvent

from ...tests.stock_stub import get_stub


class StockMetricCalculatorTest(TestCase):
    def setUp(self):
        data = get_stub()
        open_price, close_price = data['Open'].values, data['Close'].values
        high_price = data['High'].values
        period = 5
        short_ma, long_ma = 3, 6

        average_event = AverageEvent(open_price, close_price)
        self.average_event_metric = StockMetricCalculator(data, average_event)

        moving_average_event = MovingAverageEvent(open_price, close_price, high_price, short_ma, long_ma)
        self.moving_average_event_metric = StockMetricCalculator(data, moving_average_event)

        pass_resistance_line_event = PassResistanceLineEvent(open_price, period)
        self.pass_resistance_line_event_metric = StockMetricCalculator(data, pass_resistance_line_event)

        small_movement_event = SmallMovementEvent(open_price, close_price)
        self.small_movement_event_metric = StockMetricCalculator(data, small_movement_event)

        support_line_rebound_event = SupportLineReboundEvent(open_price, period)
        self.support_line_rebound_event_metric = StockMetricCalculator(data, support_line_rebound_event)

    def test_stock_metric_calculator_chance_of_rise_for_average_event(self):
        self.assertEqual(42.86, self.average_event_metric.calculate_chance_of_rise())

    def test_stock_metric_calculator_chance_of_rise_for_moving_average_event(self):
        self.assertEqual(100.0, self.moving_average_event_metric.calculate_chance_of_rise())

    def test_stock_metric_calculator_chance_of_rise_for_pass_resistance_line_event(self):
        self.assertEqual(40.0, self.pass_resistance_line_event_metric.calculate_chance_of_rise())

    def test_stock_metric_calculator_chance_of_rise_for_small_movement_event(self):
        self.assertEqual(0.0, self.small_movement_event_metric.calculate_chance_of_rise())

    def test_stock_metric_calculator_chance_of_rise_for_support_line_rebound_event(self):
        self.assertEqual(11.11, self.support_line_rebound_event_metric.calculate_chance_of_rise())

    # NOTE: Average rise percent for all events
    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_average_event(self):
        self.assertEqual(1.37, self.average_event_metric.calculate_average_rise_percent())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_moving_average_event(self):
        self.assertEqual(0.00, self.moving_average_event_metric.calculate_average_rise_percent())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_pass_resistance_line_event(self):
        self.assertEqual(2.28, self.passu_resistance_line_event_metric.calculate_average_rise_percent())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_small_movement_event(self):
        self.assertEqual(0.00, self.small_movement_event_metric.calculate_average_rise_percent())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_support_line_rebound_event(self):
        self.assertEqual(0.00, self.support_line_rebound_event_metric.calculate_average_rise_percent())

    # NOTE: Average continuous days for all events
    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_continuous_days_for_average_event(self):
        self.assertAlmostEquals(100.0, self.average_event_metric.calculate_average_continuous_days())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_continuous_days_for_moving_average_event(self):
        self.assertAlmostEquals(100.0, self.moving_average_event_metric.calculate_average_continuous_days())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_continuous_days_for_pass_resistance_line_event(self):
        self.assertAlmostEquals(100.0, self.pass_resistance_line_event_metric.calculate_average_continuous_days())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_continuous_days_for_small_movement_event(self):
        self.assertAlmostEquals(100.0, self.small_movement_event_metric.calculate_average_continuous_days())

    @skip("Fix after input from Tom")
    def test_stock_metric_calculator_average_rise_percent_for_support_line_rebound_event(self):
        self.assertEqual(0.00, self.support_line_rebound_event_metric.calculate_average_continuous_days())


if __name__ == '__main__':
    main()
