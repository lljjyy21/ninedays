# Function file
import datetime as dt
#import matplotlib.pyplot as plt
#from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import var as v

# enter stock code !!!!!!
stockName = v.stockName

# read csv file
df = pd.read_csv(stockName + '.csv', parse_dates=True, index_col=0)


# data type has 'Open', 'High', 'Low', 'Close', 'Volume'
# if want to get only few data type, use df[['Open','High']]

# data frame to list
def df_to_list(dataType):
    newList = df[dataType].tolist()
    return newList


openPriceList = df_to_list('Open')
closePriceList = df_to_list('Close')


# find percentage of event occur
def cal_percent_of_occur(eventTimes, totalTimes):
    chance = eventTimes / totalTimes
    return chance


# calculate moving average
def find_MA(Day, Range):
    closeList = df_to_list('Close')
    start = Day - Range
    end = Day
    MA = sum(closeList[start:end]) / Range
    return MA

# NOTE: check_r -> is_rise
# check today is rise or not
def check_r(Day):
    openPrice = openPriceList[Day - 1]
    closePrice = closePriceList[Day - 1]
    priceDiff = closePrice - openPrice
    if priceDiff > 0:
        return True
    else:
        return False


# NOTE: check_nextday_rise -> is_nextday_rise
# check nextday is rise or not
def check_nextday_rise(Day):
    length = len(df_to_list('Open')) - 1
    if Day > length:
        return False
    else:
        nextday = Day + 1
        return check_r(nextday)


# TODO: It can be simplified a lot!
# check end day, and make sure end day is not smaller than 0
def check_end_day(Day, Range):
    endDay = Day - Range
    if endDay < 0:
        endDay = 0
    else:
        endDay = endDay
    return endDay

# TODO: Name does not correspond to the function content!
# number of continue rise day
def count_rise_day(Day):
    riseDay = 0
    while check_nextday_rise(Day) == True:
        riseDay += 1
        Day += 1

    return riseDay

# TODO: Name does not correspond to the function content!
# sum of continue rise
def sum_of_rise(Day):
    totalSum = 0
    while check_nextday_rise(Day):
        openPrice = openPriceList[Day - 1]
        closePrice = closePriceList[Day - 1]
        totalSum = totalSum + (closePrice - openPrice) / openPrice
        Day += 1

    return totalSum




# check shortMA > longMA is True or False
def check_two_MA(Day, shortRange, longRange):
    if find_MA(Day, shortRange) > find_MA(Day, longRange):
        return True
    else:
        return False


# total number of days that shortMA > longMA  cause a rise within the tests range
def Times_shortMA_bigger_than_longMA_cause_rise(Day, shortRange, longRange, Range):
    endDay = check_end_day(Day, Range)

    numOfRise = 0
    while Day > endDay:
        if check_two_MA(Day, shortRange, longRange) == True and check_nextday_rise(Day) == True:
            numOfRise += 1

        Day -= 1

    return numOfRise


# total number of days that shortMA > longMA within the tests range
def Time_shortMA_bigger_than_longMA(Day, shortRange, longRange, Range):
    endDay = check_end_day(Day, Range)

    numOfevent = 0
    while Day > endDay:
        if check_two_MA(Day, shortRange, longRange) == True:
            numOfevent += 1

        Day -= 1

    return numOfevent


# average continue rise days that shortMA > longMA within the tests range
def Avg_rise_day_count(Day, shortRange, longRange, Range):
    endDay = check_end_day(Day, Range)

    rises = 0
    numOfRise = 0
    while Day > endDay:
        if check_two_MA(Day, shortRange, longRange) == True:
            if check_nextday_rise(Day) == True:
                numOfRise += 1
                rises = rises + count_rise_day(Day)

        Day -= 1

    return rises / numOfRise

# NOTE: Function can be simplified
# average continue rise percentage that shortMA > longMA within the tests range
def Avg_rise_percentage(Day, shortRange, longRange, Range):
    endDay = check_end_day(Day, Range)

    sumNum = 0.0000000
    numOfRise = 0
    while Day > endDay:
        if check_two_MA(Day, shortRange, longRange) == True:
            if check_nextday_rise(Day) == True:
                numOfRise += 1
                sumNum = sumNum + sum_of_rise(Day)

        Day -= 1

    return sumNum / numOfRise



    # print(Times_shortMA_bigger_than_longMA_cause_rise(1749,5,60,100))
