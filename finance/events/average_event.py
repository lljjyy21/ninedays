from .base_event import BaseEvent
import numpy as np


# TODO: Add documentation
class AverageEvent(BaseEvent):
    def __init__(self, open_price, close_price, high_price=None):
        BaseEvent.__init__(self, open_price, close_price, high_price)
        self._validate_input()
        self.rise_percentage = np.true_divide((self.close_price - self.open_price), self.open_price) * 100

    # TODO: Check this method
    def get_events_sequence(self):
        if self.rise_percentage.shape[0] == 0:
            return np.empty([0, 0], dtype=np.int8)

        average_percentage = np.mean(self.rise_percentage[self.rise_percentage > 0])
        events_sequence = np.zeros(self.rise_percentage.shape[0], dtype=np.int8)
        for i in range(0, len(self.rise_percentage)):
            if np.around(average_percentage, decimals=2) < round(self.rise_percentage[i], 2):
                events_sequence[i] = 1

        return events_sequence
