# GET STOCK DATA TO CSV FILE
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import xlsxwriter
import datetime

now = datetime.datetime.now()

# start date enter !!!!!!
syy = 2000
smm = 1
sdd = 1

# end date enter !!!!!!
eyy = now.year
emm = now.month
edd = now.day

# enter stock code !!!!!!
stockName = 'bidu'.upper()

# enter place to get data !!!!!!
datasource = 'google'

# Save as excel file(2) or csv file(1) !!!!!!
saveAsType = 1

# covert enter values to program require value for start data and end data
start = dt.datetime(syy, smm, sdd)
end = dt.datetime(eyy, emm, edd)

# get stock info and save as csv file
df = web.DataReader('NASDAQ:' + stockName, datasource, start, end)

if saveAsType == 1:
    df.to_csv(stockName + '.csv')
else:
    writer = pd.ExcelWriter('Stock Data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, stockName)
    writer.save()
