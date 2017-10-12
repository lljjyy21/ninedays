from base_event import BaseEvent
import numpy as np


# TODO: Implement
# TODO: Add documentation
class MovingAverageEvent(BaseEvent):
    def __init__(self, open_price, close_price, high_price, short_ma, long_ma):
        BaseEvent.__init__(self, open_price, close_price, high_price)
        self.short_ma = short_ma
        self.long_ma = long_ma
        self.price = self.close_price
        self._validate_input()

    def _validate_input(self):
        BaseEvent._validate_input(self)
        self._validate_and_cast_short_ma()
        self._validate_and_cast_long_ma()
        self._validate_long_ma_bigger_or_equal_than_short_ma()

    def _validate_and_cast_short_ma(self):
        try:
            self.short_ma = int(self.short_ma)
        except TypeError as e:
            raise TypeError("Short MA is not integer")

    def _validate_and_cast_long_ma(self):
        try:
            self.long_ma = int(self.long_ma)
        except TypeError as e:
            raise TypeError("Long MA is not integer")

    def _validate_long_ma_bigger_or_equal_than_short_ma(self):
        if self.short_ma > self.long_ma:
            raise ValueError("Short MA is bigger than long MA")

    def get_events_sequence(self):
        event_sequence = np.array(self.price.shape, dtype=np.int8)

        short_ma_sum, long_ma_sum = 0, 0
        for i in range(self.price.shape[0]):
            short_ma_sum += self.price[i]
            long_ma_sum += self.price[i]
            if i - self.short_ma >= 0:
                short_ma_sum -= self.price[i - self.short_ma]
            if i - self.long_ma >= 0:
                long_ma_sum -= self.price[i - self.long_ma]

            short_avg, long_avg = (1.0 * short_ma_sum)/self.short_ma, (1.0 * long_ma_sum)/self.long_ma
            if i - self.long_ma >= -1 and short_avg > long_avg:
                event_sequence[i] = 1

        return event_sequence
