from line_event import LineEvent
import numpy as np


# TODO: Add documentation
class SupportLineReboundEvent(LineEvent):
    def __init__(self, price, time_period):
        LineEvent.__init__(self, price, time_period, 'low')

    # TODO: Test this function
    def get_events_sequence(self):
        event_sequence = np.zeros(self.price.shape, dtype=np.int8)

        # TODO: It seems like a bug into algorithm
        for j in range(self.time_period, self.price.shape[0]):
            min_first_index, min_second_index = j - self.time_period, j - self.time_period + 1

            print("Initial", min_first_index, min_second_index)

            for i in range(self.time_period):
                index = i + j - self.time_period

                if round(self.price[min_first_index], 2) > round(self.price[index], 2):
                    min_second_index = min_first_index
                    min_first_index = index
                elif index != min_first_index and round(self.price[min_second_index], 2) > round(self.price[index], 2):
                    min_second_index = index

            num_days_between_peaks = min_first_index - min_second_index
            diff_price_between_peaks = 1.0 * (self.price[min_first_index] - self.price[min_second_index])
            slope = diff_price_between_peaks/num_days_between_peaks
            support_price = self.price[min_first_index] + slope * (j - min_first_index)
            support_price_coefficient = 1.05

            if support_price <= self.price[j] <= support_price*support_price_coefficient:
                event_sequence[j] = 1

        return event_sequence
