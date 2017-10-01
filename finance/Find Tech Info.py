# READ CSV FILE AND PLOT
import datetime as dt
#import matplotlib.pyplot as plt
#from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import Function as func
import var as v

#style.use('ggplot')

# enter stock code !!!!!!
stockName = v.stockName

# read csv file
df = pd.read_csv(stockName + '.csv', parse_dates=True, index_col=0)

# enter variable, if start from latest date, use day = len(df_to_list('Open'))
day = len(func.df_to_list('Open'))
maDaysShort = 5
maDaysLong = 60
range = 100

# data type has 'Open', 'High', 'Low', 'Close', 'Volume'
# if want to get only few data type, use df[['Open','High']]

# calculate moving average into csv file
#maOne = df['Close'].rolling(window=maDaysOne, min_periods=0).mean()
#maTwo = df['Close'].rolling(window=maDaysTwo, min_periods=0).mean()

# print all the data
print('\n ** Tech info for "{}"  \n'.format(v.stockName))
tnum = func.Time_shortMA_bigger_than_longMA(day,maDaysShort,maDaysLong,range)
print('In pass {} days,{} days MA overcome {} days MA {} times!'.format(range,maDaysShort,maDaysLong,tnum))
chanceofrise = (1.0 * func.Times_shortMA_bigger_than_longMA_cause_rise(day,maDaysShort,maDaysLong,range))/tnum * 100
COR = "%.2f" % chanceofrise
print('and the chance of rise occur is {}% !'.format(COR))
avgrisepercent = func.Avg_rise_percentage(day,maDaysShort,maDaysLong,range) * 100
avgp = "%.2f" % avgrisepercent
avgriseday = func.Avg_rise_day_count(day,maDaysShort,maDaysLong,range)
avgrd = "%.2f" % avgriseday
print('in average, they will rise about {}% and {} days continuously!'.format(avgp,avgrd))
#print(maOne)
#print(maTwo)

# plot all the data
#ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
#ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1)

#ax1.plot(df.index,df['Close'])
#ax1.plot(df.index,maOne)
#ax1.plot(df.index,maTwo)
#ax2.bar(df.index,df['Volume'])
#plt.show()