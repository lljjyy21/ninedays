from .base_event import BaseEvent
import numpy as np


# TODO: Add documentation
class SmallMovementEvent(BaseEvent):
    def __init__(self, open_price, close_price, high_price=None):
        BaseEvent.__init__(self, open_price, close_price, high_price)
        self.rise_percentage = None

    def _calculate_rise_percentage(self):
        self.rise_percentage = np.true_divide((self.close_price - self.open_price), self.open_price)
        self.rise_percentage = np.around(self.rise_percentage, decimals=5)

    def get_events_sequence(self):
        self._calculate_rise_percentage()
        if self.rise_percentage.shape[0] == 0:
            return np.empty([0, 0], dtype=np.int8)
        elif self.rise_percentage.shape[0] < 5:
            return np.array([0] * self.rise_percentage.shape[0], dtype=np.int8)

        events_sequence = np.zeros(self.rise_percentage.shape[0], dtype=np.int8)

        num_of_days_with_small_movement = 0
        for i in range(0, len(self.rise_percentage)):
            if num_of_days_with_small_movement > 3 and abs(self.rise_percentage[i]) > 0.01:
                events_sequence[i] = 1
                num_of_days_with_small_movement = 0
            elif abs(self.rise_percentage[i]) > 0.01:
                num_of_days_with_small_movement = 0
            else:
                num_of_days_with_small_movement += 1

        return events_sequence
