from unittest import TestCase, main
from finance.events.small_movement_event import SmallMovementEvent
import numpy as np


class SmallMovementEventTest(TestCase):

    def test_small_movement_event_with_zero_inputs(self):
        open_price, close_price = np.empty([0, 0]), np.empty([0, 0])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        expected = np.empty([0, 0], dtype=np.int8)
        self.assertTrue((expected == small_movement_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, small_movement_event.get_events_sequence().dtype)

    def test_small_movement_event_with_one_to_four_elements_lengths(self):
        for i in range(1, 5):
            open_price, close_price = np.random.rand(1, i), np.random.rand(1, i)
            small_movement_event = SmallMovementEvent(open_price, close_price)

            expected = np.array([0] * i, dtype=np.int8)
            self.assertTrue((expected == small_movement_event.get_events_sequence()).all())
            self.assertEqual(expected.dtype, small_movement_event.get_events_sequence().dtype)

    def test_small_movement_event_with_input_of_different_lengths(self):
        open_price, close_price = np.array([1.0, 2.0, 10.0, 100.0, 5.5]), np.array([2.2, 3.9, 5.0, 67.2])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        self.assertRaises(ValueError, small_movement_event.get_events_sequence)

    def test_small_movement_event_with_proper_input(self):
        open_price  = np.array([1.0, 1.0, 1.0, 1.2, 1.6, 1.0, 1.2, 1.40, 1.2, 1.6, 1.0, 1.6])
        close_price = np.array([1.01, 1.01, 1.001, 1.2, 3.6, 1.1, 1.1, 1.41, 1.2, 1.6, 1.0, 0.5])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        expected = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], dtype=np.int8)

        self.assertTrue(np.array_equal(expected, small_movement_event.get_events_sequence()))
        self.assertEqual(expected.dtype, small_movement_event.get_events_sequence().dtype)

if __name__ == '__main__':
    main()
