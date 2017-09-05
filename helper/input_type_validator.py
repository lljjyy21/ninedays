class TypeValidator(object):
    def __init__(self, start, end, short_ma, long_ma, range_in_days):
        self.start = start
        self.end = end
        self.short_ma = short_ma
        self.long_ma = long_ma
        self.range_in_days = range_in_days

    def validate(self):
        try:
            TypeValidator.validate_date(self.start)
            TypeValidator.validate_date(self.end)
            TypeValidator.validate_int(self.short_ma)
            TypeValidator.validate_int(self.long_ma)
            TypeValidator.validate_int(self.range_in_days)
        except RuntimeError as _:
            return False
        return True

    @staticmethod
    def validate_int(value):
        try:
            int(value)
        except Exception as _:
            raise RuntimeError

    @staticmethod
    def validate_date(value):
        try:
            import datetime as dt
            dt.datetime.strptime(value, '%Y-%m-%d')
        except Exception as e:
            raise RuntimeError
