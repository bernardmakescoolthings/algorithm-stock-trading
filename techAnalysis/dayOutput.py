import sys

import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import datetime, timedelta

if len(sys.argv) == 2:
    START_DATE = sys.argv[1]
    dateArr = START_DATE.split("-")
    dateObj = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]))
elif len(sys.argv) == 1:
    dateObj = datetime.today().date()
else:
    print("Error with command line arguments")
    sys.exit()

print(dateObj)

stockFile = open("stocks.txt", "r")
for stock in stockFile:
    stock = stock.split()[0]

    df = pdr.get_data_yahoo(stock, start=dateObj)
    print((df.iloc[0]["Close"] - df.iloc[0]["Open"])/ df.iloc[0]["Open"])
