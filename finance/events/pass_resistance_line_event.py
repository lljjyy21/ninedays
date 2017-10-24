from line_event import LineEvent
import numpy as np


# TODO: Add documentation
class PassResistanceLineEvent(LineEvent):
    def __init__(self, open_price, time_period):
            LineEvent.__init__(self, open_price, time_period)

    # TODO: Think if this algorithm can be reimplemented in more efficient algorithm
    def get_events_sequence(self):
        event_sequence = np.zeros((self.open_price.shape[0],), dtype=np.int8)

        for j in range(self.time_period, self.open_price.shape[0]):
            max_first_index, max_second_index = j - self.time_period, j - self.time_period + 1

            for i in range(self.time_period):
                index = i + j - self.time_period

                if round(self.open_price[max_first_index], 2) < round(self.open_price[index], 2):
                    max_second_index = max_first_index
                    max_first_index = index
                elif max_first_index != index and round(self.open_price[max_second_index], 2) < round(self.open_price[index], 2):
                    max_second_index = index
            num_days_between_peaks = max_first_index - max_second_index
            diff_price_between_peaks = 1.0 * (self.open_price[max_first_index] - self.open_price[max_second_index])
            slope = diff_price_between_peaks/num_days_between_peaks

            if self.open_price[max_first_index] + slope * (j - max_first_index) < self.open_price[j]:
                event_sequence[j] = 1

        return event_sequence
