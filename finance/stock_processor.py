import datetime as dt
import pandas_datareader.data as web
from stock_calculator import StockCalculator
#import Function as func


class StockProcessor:
    def __init__(self, stock_name, start_date, end_date, short_ma, long_ma, range_days, data_source='google'):
        self.stock = stock_name.upper()
        self.start = dt.datetime.strptime(start_date, '%Y-%m-%d')
        self.end = dt.datetime.strptime(end_date, '%Y-%m-%d')
        print("-" * 25)
        print(self.start, self.end)
        print("-" * 25)
        self.short_ma = int(short_ma)
        self.long_ma = int(long_ma)
        self.range_days = int(range_days)
        self.data_source = data_source

    def get_stock(self):
        df = web.DataReader('NASDAQ:' + self.stock, self.data_source, self.start, self.end)
        return df

    # TODO: Refactor
    def info(self):
        try:
            df = self.get_stock()
            stock_calculator = StockCalculator(df, self.short_ma, self.long_ma, self.range_days)
            day = len(stock_calculator.get_open_price_list())

            message = 'Tech info for {}\n'.format(self.stock)
            tnum = stock_calculator.num_days_short_moving_average_bigger_than_long_moving_average(day)
            message += 'In pass {} days,{} days MA overcome {} days MA {} times!\n'.format(self.range_days, self.short_ma, self.long_ma, tnum)
            chanceofrise = (1.0 * stock_calculator.num_days_short_moving_average_bigger_than_long_moving_average_cause_rise(day)) / tnum * 100

            COR = "%.2f" % chanceofrise
            message += 'and the chance of rise occur is {}% !\n'.format(COR)
            avgrisepercent = stock_calculator.average_rise_percentage(day) * 100
            avgp = "%.2f" % avgrisepercent
            avgriseday = stock_calculator.average_rises_per_day_when_short_moving_average_bigger_than_long_moving_average(day)
            avgrd = "%.2f" % avgriseday
            message += 'in average, they will rise about {}% and {} days continuously!'.format(avgp, avgrd)
        except Exception as e:
            message = "Sorry, I can't find that stock's data!"
            print(e)
        return message
