class StockCalculator:
    def __init__(self, data_frame, short_ma, long_ma, range_days):
        self.data_frame = data_frame
        self.short_ma = short_ma
        self.long_ma = long_ma
        self.range_days = range_days
        self.open_price_list = self._data_frame_to_list('Open')
        self.close_price_list = self._data_frame_to_list('Close')
        self.high_price_list = self._data_frame_to_list('High')
        self.low_price_list = self._data_frame_to_list('Low')

    def _data_frame_to_list(self, data_type):
        try:
            new_list = self.data_frame[data_type].tolist()
        except Exception as e:
            new_list = []
            print(e)
        return new_list

    @staticmethod
    def get_open_price_list(data_frame):
        stock_calculator = StockCalculator(data_frame, None, None, None)
        return stock_calculator._data_frame_to_list('Open')

    @staticmethod
    def get_close_price_list(data_frame):
        stock_calculator = StockCalculator(data_frame, None, None, None)
        return stock_calculator._data_frame_to_list('Close')

    @staticmethod
    def get_high_price_list(data_frame):
        stock_calculator = StockCalculator(data_frame, None, None, None)
        return stock_calculator._data_frame_to_list('High')

    @staticmethod
    def get_low_price_list(data_frame):
        stock_calculator = StockCalculator(data_frame, None, None, None)
        return stock_calculator._data_frame_to_list('Low')

    def calculate_percent_of_occurrence(self, num_event, num_total):
        try:
            chance = (1.0*num_event)/num_total
        except Exception as e:
            chance = 0.0
            print(e)
        return chance

    def find_moving_average(self, day, num_days_ma):
        start, end = day - num_days_ma, day
        moving_average = sum(self.close_price_list[start:end]) / num_days_ma
        return moving_average

    def is_rise(self, day):
        day -= 1
        open_price, close_price = self.open_price_list[day], self.close_price_list[day]
        price_diff = close_price - open_price
        if price_diff > 0:
            return True
        return False

    def is_nextday_rise(self, day):
        length = len(self.open_price_list) - 1
        if day > length:
            return False
        nextday = day + 1
        return self.is_rise(nextday)

    def is_end_day(self, day):
        end_day = max(day - self.range_days, 0)
        return end_day

    def count_continuous_rise_days(self, day):
        rise_days = 0
        while self.is_nextday_rise(day):
            rise_days += 1
            day += 1
        return rise_days

    def sum_of_continuous_rise_days(self, day):
        total_sum = 0
        while self.is_nextday_rise(day):
            open_price, close_price = self.open_price_list[day - 1], self.close_price_list[day - 1]
            total_sum += (1.0*(close_price - open_price)) / open_price
            day += 1
        return total_sum

    def compare_short_and_long_moving_average(self, day):
        if self.find_moving_average(day, self.short_ma) > self.find_moving_average(day, self.long_ma):
            return True
        return False

    def num_days_short_moving_average_bigger_than_long_moving_average_cause_rise(self, day):
        end_day = self.is_end_day(day)
        num_rises = 0
        while day > end_day:
            if self.compare_short_and_long_moving_average(day) and \
               self.is_nextday_rise(day):
                num_rises += 1
            day -= 1
        return num_rises

    # TODO: Extraxt day, short_ma, long_ma, range_days into __init__!
    def num_days_short_moving_average_bigger_than_long_moving_average(self, day):
        end_day = self.is_end_day(day)

        num_days = 0
        while day > end_day:
            if self.compare_short_and_long_moving_average(day):
                num_days += 1
            day -= 1

        return num_days

    def average_rises_per_day_when_short_moving_average_bigger_than_long_moving_average(self, day):
        end_day = self.is_end_day(day)

        num_days = 0
        num_nextday_rises = 0
        while day > end_day:
            if self.compare_short_and_long_moving_average(day):
                if self.is_nextday_rise(day):
                    num_nextday_rises += 1
                    num_days += self.count_continuous_rise_days(day)
            day -= 1

        return (1.0*num_nextday_rises)/num_days

    def average_rise_percentage(self, day):
        end_day = self.is_end_day(day)

        sum_rises = 0.0000000
        num_nextday_rises = 0
        while day > end_day:
            if self.compare_short_and_long_moving_average(day):
                if self.is_nextday_rise(day):
                    num_nextday_rises += 1
                    sum_rises += + self.sum_of_continuous_rise_days(day)
            day -= 1

        return sum_rises / num_nextday_rises
