class BaseEvent(object):
    def __init__(self, open_price, close_price, high_price):
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price

    def get_events_sequence(self):
        pass
