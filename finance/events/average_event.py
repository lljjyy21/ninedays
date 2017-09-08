from .base_event import BaseEvent
import numpy as np


# TODO: Add documentation
class AverageEvent(BaseEvent):
    def __init__(self, open_price, close_price, high_price=None):
        BaseEvent.__init__(self, open_price, close_price, high_price)
        self.rise_percentage = None
        self._validate_input()

    def _calculate_rise_percentage(self):
        self.rise_percentage = np.true_divide((self.close_price - self.open_price), self.open_price)

    def get_events_sequence(self):

        self._calculate_rise_percentage()
        if self.rise_percentage.shape[0] == 0:
            return np.empty([0, 0], dtype=np.int8)

        sum_percentage = self.rise_percentage[0]
        events_sequence = np.zeros(self.rise_percentage.shape[0], dtype=np.int8)
        for i in range(1, len(self.rise_percentage)):
            if (1.0 * sum_percentage)/i < self.rise_percentage[i]:
                events_sequence[i] = 1

        return events_sequence
