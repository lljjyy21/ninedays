from unittest import TestCase, main
from tests.extended_test import ExtendedTestCase
from finance.events.pass_resistance_line_event import PassResistanceLineEvent
import numpy as np


class PassResistanceLineEventTest(ExtendedTestCase):

    def test_pass_resistance_line_event_with_zero_inputs(self):
        open_price, close_price = np.empty([0, 0]), np.empty([0, 0])
        high_price = np.empty([0, 0])
        time_period = 5
        pass_resistance_line_event = PassResistanceLineEvent(open_price, close_price, high_price, time_period)

        expected = np.empty([0, 0], dtype=np.int8)
        self.assertTrue((expected == pass_resistance_line_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, pass_resistance_line_event.get_events_sequence().dtype)

    def test_pass_resistance_line_event_with_one_to_time_period_elements_lengths(self):
        time_periods = np.array([5, 10, 15])
        for time_period in time_periods:
            for i in range(1, time_period):
                open_price = np.random.rand(i)
                close_price = np.random.rand(i)
                high_price = np.random.rand(i)

                pass_resistance_line_event = PassResistanceLineEvent(open_price, close_price, high_price, time_period)

                expected = np.zeros(i, dtype=np.int8)
                real = pass_resistance_line_event.get_events_sequence()

                self.assertEqual(expected.shape, real.shape)
                self.assertTrue((expected == real).all())
                self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_proper_input(self):
        high_price = np.array([10.0, 11.0, 16.0, 15.0, 13.0, 13.0, 12.0, 13.5, 12.95, 14.0, 12.0])
        time_period = 5
        pass_resistance_line_event = PassResistanceLineEvent(None, None, high_price, time_period)

        expected = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_another_proper_input(self):
        high_price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        time_period = 5
        pass_resistance_line_event = PassResistanceLineEvent(None, None, high_price, time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_wrong_high_price_input(self):
        time_period = 5
        open_price, close_price = None, None
        high_price = None

        self.assertRaises(TypeError, PassResistanceLineEvent, open_price, close_price, high_price, time_period)
        self.assertRaisesWithMessage("High price is not numpy array",
                                     PassResistanceLineEvent, open_price, close_price, high_price, time_period)

    def test_pass_resistance_line_event_with_wrong_time_period_input(self):
        open_price, close_price = None, None
        high_price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        time_periods = [-1000, -1, 0, 1]
        for time_period in time_periods:
            self.assertRaises(ValueError, PassResistanceLineEvent, open_price, close_price, high_price, time_period)
            self.assertRaisesWithMessage("Time period is less than 2 days",
                                         PassResistanceLineEvent, open_price, close_price, high_price, time_period)

        time_period = None
        self.assertRaises(TypeError, PassResistanceLineEvent, open_price, close_price, high_price, time_period)
        self.assertRaisesWithMessage("Time period is not int",
                                     PassResistanceLineEvent, open_price, close_price, high_price, time_period)


if __name__ == '__main__':
    main()
