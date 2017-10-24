import numpy as np


class BaseEvent(object):
    def __init__(self, open_price, close_price=None, high_price=None, low_price=None):
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price

    def get_events_sequence(self):
        pass

    def _validate_input(self):
        self._validate_open_price()
        self._validate_close_price()
        self._validate_open_and_close_prices_shapes()

    def _validate_open_price(self):
        if type(self.open_price) is not np.ndarray:
            raise TypeError("Open price is not numpy array")

    def _validate_close_price(self):
        if type(self.close_price) is not np.ndarray:
            raise TypeError("Close price is not numpy array")

    def _validate_open_and_close_prices_shapes(self):
        if self.open_price.shape != self.close_price.shape:
            raise ValueError("Open price and close price arrays are different shapes")
