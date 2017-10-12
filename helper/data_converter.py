import datetime

class DataConverter(object):

    def __init__(self, start, end, short_ma, long_ma, range_in_days):
        self.start = self._to_date(start)
        self.end = self._to_date(end)
        self.short_ma = self._to_int(short_ma)
        self.long_ma = self._to_int(long_ma)
        self.range_in_days = self._to_int(range_in_days)

    def _to_date(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def _to_int(self, integer):
        return int(integer)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_short_ma(self):
        return self.short_ma

    def get_long_ma(self):
        return self.long_ma

    def get_range(self):
        return self.range_in_days
