from line_event import LineEvent
import numpy as np


# TODO: Add documentation
class PassResistanceLineEvent(LineEvent):
    def __init__(self, price, time_period):
            LineEvent.__init__(self, price, time_period)

    # TODO: Think if this algorithm can be reimplemented in more efficient algorithm
    def get_events_sequence(self):
        event_sequence = np.zeros((self.price.shape[0],), dtype=np.int8)

        for j in range(self.time_period, self.price.shape[0]):
            # TODO: DEBUG this code accurately one more time
            max_first_index, max_second_index = j - self.time_period, j - self.time_period + 1

            # print("Initial", max_first_index, max_second_index)

            for i in range(self.time_period):
                index = i + j - self.time_period

                if round(self.price[max_first_index], 2) < round(self.price[index], 2):
                    max_second_index = max_first_index
                    max_first_index = index
                elif max_first_index != index and round(self.price[max_second_index], 2) < round(self.price[index], 2):
                    max_second_index = index
            num_days_between_peaks = max_first_index - max_second_index
            diff_price_between_peaks = 1.0 * (self.price[max_first_index] - self.price[max_second_index])
            slope = diff_price_between_peaks/num_days_between_peaks

            # print(max_first_index, max_second_index)

            if self.price[max_first_index] + slope * (j - max_first_index) < self.price[j]:
                event_sequence[j] = 1

        return event_sequence
