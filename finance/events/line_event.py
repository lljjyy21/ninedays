from .base_event import BaseEvent
import numpy as np


class LineEvent(BaseEvent):
    def __init__(self, open_price, time_period):
        BaseEvent.__init__(self, open_price)
        self.time_period = time_period
        self._validate_input()

    def _validate_input(self):
        self._validate_price()
        self._validate_time_period()

    def _validate_price(self):
        if type(self.open_price) is not np.ndarray:
            raise TypeError("Price is not numpy array")

    def _validate_time_period(self):
        if not isinstance(self.time_period, (int, long)):
            raise TypeError("Time period is not int")
        if self.time_period < 2:
            raise ValueError("Time period is less than 2 days")
