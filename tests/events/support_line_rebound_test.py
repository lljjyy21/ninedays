# coding=utf-8
from unittest import main
from ...tests.extended_test import ExtendedTestCase
from ...finance.events.support_line_rebound_event import SupportLineReboundEvent
import numpy as np


# TODO: Add documentation
class SupportLineReboundEventTest(ExtendedTestCase):

    def setUp(self):
        self.event_class_name = 'support-rebound-line-event'
        self.description = u'Support line rebound (S line): Similar to the (R line) event, just change the highest ' \
                           u'price to lowest price. The event happens when today’s price is within ' \
                           u'support price × 1.05 and support price'
        self.price = np.empty([0, 0])
        self.time_period = 5

    def test_support_line_rebound_metadata(self):
        support_line_rebound_event = SupportLineReboundEvent(self.price, self.time_period)

        self.assertEqual(support_line_rebound_event.class_name, self.event_class_name)
        self.assertEqual(support_line_rebound_event.description, self.description)

    def test_support_line_rebound_zero_inputs(self):
        support_line_rebound_event = SupportLineReboundEvent(self.price, self.time_period)

        expected = np.empty([0, 0], dtype=np.int8)

        self.assertEqual(support_line_rebound_event.get_events_sequence().shape, expected.shape)
        self.assertTrue((expected == support_line_rebound_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, support_line_rebound_event.get_events_sequence().dtype)

    def test_pass_resistance_line_event_with_wrong_high_price_input(self):
        price = None

        self.assertRaises(TypeError, SupportLineReboundEvent, price, self.time_period)
        self.assertRaisesWithMessage("Price is not numpy array",
                                     SupportLineReboundEvent, price, self.time_period)

    def test_pass_resistance_line_event_with_wrong_time_period_input(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])
        time_periods = [-1000, -1, 0, 1]
        for time_period in time_periods:
            self.assertRaises(ValueError, SupportLineReboundEvent, price, time_period)
            self.assertRaisesWithMessage("Time period is less than 2 days",
                                         SupportLineReboundEvent, price, time_period)

        time_period = None
        self.assertRaises(TypeError, SupportLineReboundEvent, price, time_period)
        self.assertRaisesWithMessage("Time period is not int",
                                     SupportLineReboundEvent, price, time_period)

    def test_pass_resistance_line_event_with_proper_input(self):
        price = np.array([10.0, 10.0, 10.0, 10.0, 10.0, 10.5, 10.5, 10.5])
        support_line_rebound_event = SupportLineReboundEvent(price, self.time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 1, 1], dtype=np.int8)
        real = support_line_rebound_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_pass_resistance_line_event_with_another_proper_input(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 15.01, 10.0, 11.0, 11.0, 12.0, 14.7])
        support_line_rebound_event = SupportLineReboundEvent(price, self.time_period)

        expected = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.int8)
        real = support_line_rebound_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)


if __name__ == '__main__':
    main()
