import numpy as np


class BaseEvent(object):
    class_name = 'base-event'
    description = ''

    def __init__(self, open_price, close_price=None):
        self.open_price = open_price
        self.close_price = close_price

    def get_events_sequence(self):
        pass

    def event_triggered_at_the_last_date(self):
        event_sequence = self.get_events_sequence()
        return ["No", "Yes"][len(event_sequence) > 0 and event_sequence[-1] == 1]

    def get_event_metadata(self):
        return {'description': self.description,
                'class-name': self.class_name}

    def _validate_input(self):
        self._validate_open_price()
        self._validate_close_price()
        self._validate_open_and_close_prices_shapes()
        return

    def _validate_open_price(self):
        if type(self.open_price) is not np.ndarray:
            raise TypeError("Open price is not numpy array")
        return

    def _validate_close_price(self):
        if type(self.close_price) is not np.ndarray:
            raise TypeError("Close price is not numpy array")
        return

    def _validate_open_and_close_prices_shapes(self):
        if self.open_price.shape != self.close_price.shape:
            raise ValueError("Open price and close price arrays are different shapes")
        return
