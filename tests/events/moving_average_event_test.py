from unittest import main, skip
from ...tests.extended_test import ExtendedTestCase
from ...finance.events.moving_average_event import MovingAverageEvent
import numpy as np


# TODO: Add documentation

# TODO: Add proper tests after Tom's response
class MovingAverageEventTest(ExtendedTestCase):

    @skip("while moving average is not ready")
    def test_support_line_rebound_zero_inputs(self):
        pass

    @skip("while moving average is not ready")
    def test_moving_average_event_with_wrong_high_price_input(self):
        pass
        """
        time_period = 5
        low_price = None

        self.assertRaises(TypeError, MovingAverageEvent, low_price, time_period)
        self.assertRaisesWithMessage("Low price is not numpy array",
                                     MovingAverageEvent, low_price, time_period)
        """

    @skip("while moving average is not ready")
    def test_pass_resistance_line_event_with_wrong_time_period_input(self):
        pass
        """
        low_price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        time_periods = [-1000, -1, 0, 1]
        for time_period in time_periods:
            self.assertRaises(ValueError, MovingAverageEvent, low_price, time_period)
            self.assertRaisesWithMessage("Time period is less than 2 days",
                                         MovingAverageEvent, low_price, time_period)

        time_period = None
        self.assertRaises(TypeError, MovingAverageEvent, low_price, time_period)
        self.assertRaisesWithMessage("Time period is not int",
                                     MovingAverageEvent, low_price, time_period)
        """

    @skip("while moving average is not ready")
    def test_pass_resistance_line_event_with_proper_input(self):
        pass

        """
        low_price = np.array([10.0, 10.0, 10.0, 10.0, 10.0, 10.5, 10.5, 10.5])
        time_period = 5
        pass_resistance_line_event = MovingAverageEvent(low_price, time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 1, 1], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        print(expected)
        print(real)

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)
        """

    @skip("while moving average is not ready")
    def test_pass_resistance_line_event_with_another_proper_input(self):
        pass

        """
        low_price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 15.01, 10.0, 11.0, 11.0, 12.0, 14.7])
        time_period = 5
        pass_resistance_line_event = MovingAverageEvent(low_price, time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        print(expected)
        print(real)

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)
        """


if __name__ == '__main__':
    main()
