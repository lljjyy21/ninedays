# coding=utf-8
from line_event import LineEvent
import numpy as np


# TODO: Add documentation
class SupportLineReboundEvent(LineEvent):
    class_name = 'support-line-rebound-event'
    description = u'Support line rebound (S line): Similar to the (R line) event, just change the highest price to ' \
                  u'lowest price. The event happens when today’s price is within support price × 1.05 and support price'

    def __init__(self, open_price, time_period):
        LineEvent.__init__(self, open_price, time_period)

    def get_events_sequence(self):
        event_sequence = np.zeros(self.open_price.shape, dtype=np.int8)

        for j in range(self.time_period, self.open_price.shape[0]):
            min_first_index, min_second_index = j - self.time_period, j - self.time_period + 1

            for i in range(self.time_period):
                index = i + j - self.time_period

                if round(self.open_price[min_first_index], 2) > round(self.open_price[index], 2):
                    min_second_index = min_first_index
                    min_first_index = index
                elif index != min_first_index and round(self.open_price[min_second_index], 2) > round(self.open_price[index], 2):
                    min_second_index = index

            num_days_between_peaks = min_first_index - min_second_index
            diff_price_between_peaks = 1.0 * (self.open_price[min_first_index] - self.open_price[min_second_index])
            slope = diff_price_between_peaks/num_days_between_peaks
            support_price = self.open_price[min_first_index] + slope * (j - min_first_index)
            support_price_coefficient = 1.05

            if support_price <= self.open_price[j] <= support_price*support_price_coefficient:
                event_sequence[j] = 1

        return event_sequence
