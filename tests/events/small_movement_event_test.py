# coding=utf-8
from unittest import main
from ...tests.extended_test import ExtendedTestCase
from ...finance.events.small_movement_event import SmallMovementEvent
import numpy as np


class SmallMovementEventTest(ExtendedTestCase):

    def setUp(self):
        self.event_class_name = 'small-movement-event'
        self.description = u'Small movement (SM): Basic requirement: when the total stock price percentage change is ' \
                           u'less than 1 percent (± 1%) for more than 3 business days. Event triggers when today' \
                           u' day\'s stock price percentage change is more than 1%.'
        self.open_price, self.close_price = np.empty([0, 0]), np.empty([0, 0])
        self.yes, self.no = "Yes", "No"

    def test_small_movement_event_metadata(self):
        small_movement_event = SmallMovementEvent(self.open_price, self.close_price)

        self.assertEqual(small_movement_event.class_name, self.event_class_name)
        self.assertEqual(small_movement_event.description, self.description)

    def test_small_movement_event_with_zero_inputs(self):
        small_movement_event = SmallMovementEvent(self.open_price, self.close_price)

        expected = np.empty([0, 0], dtype=np.int8)

        self.assertTrue((expected == small_movement_event.get_events_sequence()).all())
        self.assertEqual(expected.dtype, small_movement_event.get_events_sequence().dtype)

    def test_small_movement_event_with_one_to_four_elements_lengths(self):
        for i in range(1, 5):
            open_price, close_price = np.random.rand(i), np.random.rand(i)
            small_movement_event = SmallMovementEvent(open_price, close_price)

            expected = np.zeros(i, dtype=np.int8)
            real = small_movement_event.get_events_sequence()

            self.assertEqual(expected.shape, real.shape)
            self.assertTrue((expected == real).all())
            self.assertEqual(expected.dtype, real.dtype)

    def test_small_movement_event_with_input_of_different_lengths(self):
        open_price, close_price = np.array([1.0, 2.0, 10.0, 100.0, 5.5]), np.array([2.2, 3.9, 5.0, 67.2])

        self.assertRaises(ValueError, SmallMovementEvent, open_price, close_price)
        self.assertRaisesWithMessage("Open price and close price arrays are different shapes",
                                     SmallMovementEvent, open_price, close_price)

    def test_small_movement_event_with_wrong_input(self):
        open_price, close_price = None, None

        self.assertRaises(TypeError, SmallMovementEvent, open_price, close_price)
        self.assertRaisesWithMessage("Open price is not numpy array",
                                     SmallMovementEvent, open_price, close_price)

        open_price = np.empty([0, 0])
        self.assertRaises(TypeError, SmallMovementEvent, open_price, close_price)
        self.assertRaisesWithMessage("Close price is not numpy array",
                                     SmallMovementEvent, open_price, close_price)

    def test_small_movement_event_with_proper_input(self):
        open_price = np.array([1.0, 1.0, 1.0, 1.2, 1.6, 1.0, 1.2, 1.40, 1.2, 1.6, 1.0, 1.6])
        close_price = np.array([1.01, 1.01, 1.001, 1.2, 3.6, 1.1, 1.1, 1.41, 1.2, 1.6, 1.0, 0.5])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        expected = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], dtype=np.int8)

        self.assertTrue(np.array_equal(expected, small_movement_event.get_events_sequence()))
        self.assertEqual(expected.dtype, small_movement_event.get_events_sequence().dtype)

    def test_small_movement_event_triggered_at_the_last_date_when_triggered(self):
        open_price = np.array([1.0, 1.0, 1.0, 1.2, 1.6, 1.0, 1.2, 1.40, 1.2, 1.6, 1.0, 1.6])
        close_price = np.array([1.01, 1.01, 1.001, 1.2, 3.6, 1.1, 1.1, 1.41, 1.2, 1.6, 1.0, 0.5])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        self.assertEqual(self.yes, small_movement_event.event_triggered_at_the_last_date())

    def test_small_movement_event_triggered_at_the_last_date_when_not_triggered(self):
        open_price = np.array([1.0, 1.0, 1.0, 1.2, 1.6, 1.0, 1.2, 1.40, 1.2, 1.6, 1.0, 1.6])
        close_price = np.array([1.01, 1.01, 1.001, 1.2, 3.6, 1.1, 1.1, 1.41, 1.2, 1.6, 1.0, 1.6])
        small_movement_event = SmallMovementEvent(open_price, close_price)

        self.assertEqual(self.no, small_movement_event.event_triggered_at_the_last_date())

    def test_small_movement_event_triggered_at_the_last_date_when_no_data(self):
        small_movement_event = SmallMovementEvent(self.open_price, self.close_price)

        self.assertEqual(self.no, small_movement_event.event_triggered_at_the_last_date())


if __name__ == '__main__':
    main()
