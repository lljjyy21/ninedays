from unittest import TestCase, main
from finance.events.average_event import AverageEvent
import numpy as np


class AverageEventTest(TestCase):

    def test_average_event_with_zero_inputs(self):
        open_price, close_price = np.empty([0, 0]), np.empty([0, 0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.empty([0, 0], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_with_one_inputs(self):
        open_price, close_price = np.array([1.0]), np.array([2.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_on_sequence(self):
        open_price, close_price = np.array([1.0, 2.0, 3.0, 3.0, 5.0, 5.0]), np.array([2.0, 3.0, 4.0, 10.0, 5.0, 10.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 1, 0, 1], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_on_increasing_sequence(self):
        open_price, close_price = np.array([1.0, 1.0, 1.0, 1.0]), np.array([2.0, 2.1, 2.2, 2.3])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 1, 1, 1], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_on_stable_sequence(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.0, 7.0, 6.0, 5.0, 4.0])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 0, 0, 0], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_on_decreasing_sequence(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.1, 7.2, 6.3, 5.4, 4.5])
        average_event = AverageEvent(open_price, close_price, None)

        expected = np.array([0, 0, 0, 0, 0, 0], dtype=np.int8)
        self.assertTrue((expected == average_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, average_event.get_events_sequence().dtype)

    def test_average_event_with_input_input_of_different_lengths(self):
        open_price, close_price = np.array([10.0, 9.0, 8.0, 7.0, 6.0, 5.0]), np.array([9.0, 8.1])
        average_event = AverageEvent(open_price, close_price, None)

        self.assertRaises(ValueError, average_event.get_events_sequence)

if __name__ == '__main__':
    main()
