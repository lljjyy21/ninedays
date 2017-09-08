from finance.events.base_event import BaseEvent
import numpy as np


# TODO: Add documentation
class PassResistanceLineEvent(BaseEvent):
    def __init__(self, open_price, close_price, high_price, time_period):
            BaseEvent.__init__(self, open_price, close_price, high_price)
            self.time_period = time_period

    # TODO: Re-implement with different from brute-force algorithm
    def get_events_sequence(self):
        if type(self.high_price) is not np.ndarray:
            raise TypeError("High price is not numpy array")
        if not isinstance(self.time_period, (int, long)):
            raise TypeError("Time period is not int")
        if self.time_period < 2:
            raise ValueError("Time period is less than 2 days")

        event_sequence = np.zeros((self.high_price.shape[0],), dtype=np.int8)

        for j in range(self.time_period, self.high_price.shape[0]):
            max_first_index, max_second_index = 0, 1
            for i in range(self.time_period):
                if self.high_price[max_first_index] < self.high_price[i + j - self.time_period]:
                    max_second_index = max_first_index
                    max_first_index = i + j - self.time_period
                elif self.high_price[max_second_index] < self.high_price[i + j - self.time_period]:
                    max_second_index = i + j - self.time_period
            num_days_between_peaks = max_first_index - max_second_index
            diff_price_between_peaks = 1.0 * (self.high_price[max_first_index] - self.high_price[max_second_index])
            slope = diff_price_between_peaks/num_days_between_peaks

            if self.high_price[max_first_index] + slope * (j - max_first_index) < self.high_price[j]:
                event_sequence[j] = 1

        return event_sequence
