# coding=utf-8
from unittest import TestCase, main
from ...tests.extended_test import ExtendedTestCase
from ...finance.events.pass_resistance_line_event import PassResistanceLineEvent
import numpy as np


class PassResistanceLineEventTest(ExtendedTestCase):

    def setUp(self):
        self.event_class_name = 'pass-resistance-line-event'
        self.description = u'Pass Resistance line (R line): Connect 2 highest price in a specific period will create ' \
                           u'the Resistance line, the price difference divides the days between two points can get ' \
                           u'the slope of the line, which uses ' \
                           u'[number of (days between today and the one of the peak price date)], [the slope] and the ' \
                           u'[date and price of one of the peak price] can be used to calculate today’s ' \
                           u'resistance price. The event happens when today’s price is higher than the resistance price'
        self.price = np.empty([0, 0])
        self.time_period = 5

    def test_pass_resistance_line_event_metadata(self):
        pass_resistance_line_event = PassResistanceLineEvent(self.price, self.time_period)

        self.assertEqual(pass_resistance_line_event.class_name, self.event_class_name)
        self.assertEqual(pass_resistance_line_event.description, self.description)

    def test_pass_resistance_line_event_with_zero_inputs(self):
        pass_resistance_line_event = PassResistanceLineEvent(self.price, self.time_period)

        expected = np.empty([0, 0], dtype=np.int8)

        self.assertEqual(pass_resistance_line_event.get_events_sequence().shape, expected.shape)
        self.assertTrue((expected == pass_resistance_line_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, pass_resistance_line_event.get_events_sequence().dtype)

    def test_pass_resistance_line_event_with_one_to_time_period_elements_lengths(self):
        time_periods = np.array([5, 10, 15])
        for time_period in time_periods:
            for i in range(1, time_period):
                price = np.random.rand(i)

                pass_resistance_line_event = PassResistanceLineEvent(price, time_period)

                expected = np.zeros(i, dtype=np.int8)
                real = pass_resistance_line_event.get_events_sequence()

                self.assertEqual(expected.shape, real.shape)
                self.assertTrue((expected == real).all())
                self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_proper_input(self):
        price = np.array([10.0, 11.0, 16.0, 15.0, 13.0, 13.0, 12.0, 13.5, 12.95, 14.0, 12.0])
        pass_resistance_line_event = PassResistanceLineEvent(price, self.time_period)

        expected = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_another_proper_input(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        pass_resistance_line_event = PassResistanceLineEvent(price, self.time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.int8)
        real = pass_resistance_line_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_wrong_high_price_input(self):
        price = None

        self.assertRaises(TypeError, PassResistanceLineEvent, price, self.time_period)
        self.assertRaisesWithMessage("Price is not numpy array",
                                     PassResistanceLineEvent, price, self.time_period)

    def test_pass_resistance_line_event_with_wrong_time_period_input(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        time_periods = [-1000, -1, 0, 1]
        for time_period in time_periods:
            self.assertRaises(ValueError, PassResistanceLineEvent, price, time_period)
            self.assertRaisesWithMessage("Time period is less than 2 days",
                                         PassResistanceLineEvent, price, time_period)

        time_period = None
        self.assertRaises(TypeError, PassResistanceLineEvent, price, time_period)
        self.assertRaisesWithMessage("Time period is not int",
                                     PassResistanceLineEvent, price, time_period)


if __name__ == '__main__':
    main()
