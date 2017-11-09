# coding: utf-8
from unittest import main, skip
from ...tests.extended_test import ExtendedTestCase
from ...finance.events.moving_average_event import MovingAverageEvent
import numpy as np


# TODO: Add documentation
class MovingAverageEventTest(ExtendedTestCase):

    def setUp(self):
        self.event_class_name = 'moving-average-event'
        self.description = u'Moving average (MA): When short period moving average price is higher than long period ' \
                           u'moving average price. Two MA periods are changeable based on user input'
        self.price = np.empty([0, 0])
        self.short_ma, self.long_ma = 3, 6
        self.yes, self.no = "Yes", "No"

    def test_moving_average_event_metadata(self):
        moving_average_event = MovingAverageEvent(self.price, self.short_ma, self.long_ma)

        self.assertEqual(moving_average_event.class_name, self.event_class_name)
        self.assertEqual(moving_average_event.description, self.description)

    def test_moving_average_event_zero_inputs(self):
        moving_average_event = MovingAverageEvent(self.price, self.short_ma, self.long_ma)

        expected = np.array([], dtype=np.int8)
        real = moving_average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_moving_average_event_with_wrong_price_input(self):
        price = None

        self.assertRaises(TypeError, MovingAverageEvent, price, self.short_ma, self.long_ma)
        self.assertRaisesWithMessage("Price is not numpy array",
                                     MovingAverageEvent, price, self.short_ma, self.long_ma)

    def test_moving_average_event_with_wrong_ma_inputs(self):

        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 20.0, 10.0, 11.0, 11.0, 12.0, 15.0])

        short_ma, long_ma = -1, 10
        self.assertRaises(ValueError, MovingAverageEvent, price, short_ma, long_ma)
        self.assertRaisesWithMessage("Short MA should be, at least, 1 day long",
                                     MovingAverageEvent, price, short_ma, long_ma)

        short_ma, long_ma = 5, -1
        self.assertRaises(ValueError, MovingAverageEvent, price, short_ma, long_ma)
        self.assertRaisesWithMessage("Long MA should be, at least, 1 day long",
                                     MovingAverageEvent, price, short_ma, long_ma)

        short_ma, long_ma = 3, 3
        self.assertRaises(ValueError, MovingAverageEvent, price, short_ma, long_ma)
        self.assertRaisesWithMessage("Short MA is bigger or equal than long MA",
                                     MovingAverageEvent, price, short_ma, long_ma)

        short_ma, long_ma = 4, 3
        self.assertRaises(ValueError, MovingAverageEvent, price, short_ma, long_ma)
        self.assertRaisesWithMessage("Short MA is bigger or equal than long MA",
                                     MovingAverageEvent, price, short_ma, long_ma)

        wrong_long_mas = [None, (), [], {}, dict(), np.empty([0, 0])]
        short_ma = 2

        for long_ma in wrong_long_mas:
            self.assertRaises(TypeError, MovingAverageEvent, price, short_ma, long_ma)
            self.assertRaisesWithMessage("Long MA is not integer",
                                         MovingAverageEvent, price, short_ma, long_ma)

    def test_moving_average_event_with_proper_input(self):
        price = np.array([9.0, 10.0, 10.0, 10.0, 10.0, 10.5, 10.5, 10.5, 10.5])
        short_ma, long_ma = 2, 4

        moving_average_event = MovingAverageEvent(price, short_ma, long_ma)

        expected = np.array([0, 0, 0, 1, 0, 1, 1, 1, 0], dtype=np.int8)
        real = moving_average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_moving_average_event_with_another_proper_input(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 15.01, 10.0, 11.0, 11.0, 12.0, 14.7])
        short_ma, long_ma = 2, 5
        moving_average_event = MovingAverageEvent(price, short_ma, long_ma)

        expected = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], dtype=np.int8)
        real = moving_average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_moving_average_event_triggered_at_the_last_date_when_triggered(self):
        price = np.array([10.0, 11.0, 15.0, 16.0, 12.0, 15.01, 10.0, 11.0, 11.0, 12.0, 14.7])
        short_ma, long_ma = 2, 5
        moving_average_event = MovingAverageEvent(price, short_ma, long_ma)

        self.assertEqual(self.yes, moving_average_event.event_triggered_at_the_last_date())

    def test_moving_average_event_triggered_at_the_last_date_when_not_triggered(self):
        price = np.array([9.0, 10.0, 10.0, 10.0, 10.0, 10.5, 10.5, 10.5, 10.5])
        short_ma, long_ma = 2, 4
        moving_average_event = MovingAverageEvent(price, short_ma, long_ma)

        self.assertEqual(self.no, moving_average_event.event_triggered_at_the_last_date())

    def test_moving_average_event_triggered_at_the_last_date_when_no_data(self):
        moving_average_event = MovingAverageEvent(self.price, self.short_ma, self.long_ma)

        self.assertEqual(self.no, moving_average_event.event_triggered_at_the_last_date())


if __name__ == '__main__':
    main()
