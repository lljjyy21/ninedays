from .base_event import BaseEvent


class LineEvent(BaseEvent):
    def __init__(self, price, time_period, price_value='high'):
        if price_value == 'high':
            BaseEvent.__init__(self, None, None, price, None)
        else:
            BaseEvent.__init__(self, None, None, None, price)
        self.price_value = price_value
        self.time_period = time_period
        self._validate_input()
        self.price = price

    def _validate_input(self):
        if self.price_value == 'high':
            self._validate_high_price()
        else:
            self._validate_low_price()
        self._validate_time_period()

    def _validate_time_period(self):
        if not isinstance(self.time_period, (int, long)):
            raise TypeError("Time period is not int")
        if self.time_period < 2:
            raise ValueError("Time period is less than 2 days")
