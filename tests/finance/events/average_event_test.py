from unittest import main
from tests.extended_test import ExtendedTestCase
from finance.events.average_event import AverageEvent
import numpy as np


class AverageEventTest(ExtendedTestCase):

    def test_average_event_with_zero_inputs(self):
        open_price, close_price = np.empty([0, 0]), np.empty([0, 0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.empty([0, 0], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_with_one_inputs(self):
        open_price, close_price = np.array([1.0]), np.array([2.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_on_sequence(self):
        open_price, close_price = np.array([1.0, 2.0, 3.0, 3.0, 5.0, 5.0]), np.array([2.0, 3.0, 4.0, 10.0, 5.0, 10.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 1, 0, 1], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_on_increasing_sequence(self):
        open_price, close_price = np.array([1.0, 1.0, 1.0, 1.0]), np.array([2.0, 2.1, 2.2, 2.3])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 1, 1, 1], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_on_stable_sequence(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.0, 7.0, 6.0, 5.0, 4.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 0, 0, 0], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_on_decreasing_sequence(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.1, 7.2, 6.3, 5.4, 4.5])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 0, 0, 0], dtype=np.int8)
        real = average_event.get_events_sequence()

        self.assertEqual(expected.shape, real.shape)
        self.assertTrue((expected == real).all())
        self.assertEqual(expected.dtype, real.dtype)

    def test_average_event_with_input_input_of_different_lengths(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.1])

        self.assertRaises(ValueError, AverageEvent, open_price, close_price)
        self.assertRaisesWithMessage("Open price and close price arrays are different shapes",
                                     AverageEvent, open_price, close_price)

    def test_average_event_with_wrong_inputs(self):
        open_price, close_price = (None, None)
        self.assertRaises(TypeError, AverageEvent, open_price, close_price)
        self.assertRaisesWithMessage("Open price is not numpy array",
                                     AverageEvent, open_price, close_price)

        open_price = np.empty([0, 0])
        self.assertRaises(TypeError, AverageEvent, open_price, close_price)
        self.assertRaisesWithMessage("Close price is not numpy array",
                                     AverageEvent, open_price, close_price)

if __name__ == '__main__':
    main()
