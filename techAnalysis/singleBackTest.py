import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import ta
import sys
import math
import copy

import datetime
from datetime import datetime, timedelta

from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.decomposition import PCA

#Supress Warnings
import warnings
warnings.filterwarnings("ignore")

import yfinance as yf

if len(sys.argv) != 4:
    print("Error with command line arguments")
    sys.exit()
else:
    STOCK = sys.argv[1]
    PERIOD = int(sys.argv[2])
    START_DATE = sys.argv[3]

TARGET_PERIOD = 1

def sub_business_days(from_date, sub_days):
    business_days_to_sub = sub_days
    current_date = from_date
    while business_days_to_sub > 0:
        current_date -= timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_sub -= 1
    return current_date

def populateDataframe(df):

    # ## Momentum Indicators
    df['Awesome'] = ta.momentum.ao(df['High'], df['Low'])
    df['KAMA'] = ta.momentum.kama(df['Close'])
    df['MFI'] = ta.momentum.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'])
    df['ROC'] = ta.momentum.roc(df['Close'])
    df['RSI'] = ta.momentum.rsi(df['Close'])
    df['Stochastic'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
    df['Stochastic Signal'] = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])
    df['TSIIndicator'] = ta.momentum.tsi(df['Close'])
    df['Ultimate'] = ta.momentum.uo(df['High'], df['Low'], df['Close'])
    df['WilliamsRI'] = ta.momentum.wr(df['High'], df['Low'], df['Close'])
    df['kama'] = ta.momentum.kama(df['Close'])
    # ## Volume Indicators
    df['ADI'] = ta.volume.acc_dist_index(df['High'], df['Low'], df['Close'], df['Volume'])
    df['ChaikinMF'] = ta.volume.chaikin_money_flow(df['High'], df['Low'], df['Close'], df['Volume'])
    df['EOM'] = ta.volume.ease_of_movement(df['High'], df['Low'], df['Volume'])
    df['ForceIndex'] = ta.volume.force_index(df['Close'], df['Volume'])
    df['NVI'] = ta.volume.negative_volume_index(df['Close'], df['Volume'])
    df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
    df['EoM'] = ta.volume.sma_ease_of_movement(df['High'], df['Low'], df['Volume'])
    df['VPT'] = ta.volume.volume_price_trend(df['Close'], df['Volume'])
    df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
    df['BolllingerHigh'] = ta.volatility.bollinger_hband(df['Close'])
    df['BollingerHighIndicator'] = ta.volatility.bollinger_hband_indicator(df['Close'])
    df['BollingerLow'] = ta.volatility.bollinger_lband(df['Close'])
    df['BollingerLowIndicator'] = ta.volatility.bollinger_lband_indicator(df['Close'])
    df['BollingerBandMovingAverage'] = ta.volatility.bollinger_mavg(df['Close'])
    df['DonchianHigh'] = ta.volatility.donchian_channel_hband(df['Close'])
    df['DonchianHighIndicator'] = ta.volatility.donchian_channel_hband_indicator(df['Close'])
    df['DonchianLow'] = ta.volatility.donchian_channel_lband(df['Close'])
    df['DonchianLowIndicator'] = ta.volatility.donchian_channel_lband_indicator(df['Close'])
    df['KeltnerChannelCentral'] = ta.volatility.keltner_channel_central(df['High'], df['Low'], df['Close'])
    df['KeltnerChannelHigh'] = ta.volatility.keltner_channel_hband(df['High'], df['Low'], df['Close'])
    df['KeltnerChannelHighIndicator'] = ta.volatility.keltner_channel_hband_indicator(df['High'], df['Low'], df['Close'])
    df['KeltnerChannelLow'] = ta.volatility.keltner_channel_lband(df['High'], df['Low'], df['Close'])
    df['KeltnerChannelLowIndicator'] = ta.volatility.keltner_channel_lband_indicator(df['High'], df['Low'], df['Close'])
    # ## Trend Indicators
    #df['ADX'] = ta.trend.adx(df['High'], df['Low'], df['Close'])
    df['ADXNeg'] = ta.trend.adx_neg(df['High'], df['Low'], df['Close'])
    df['ADXPos'] = ta.trend.adx_pos(df['High'], df['Low'], df['Close'])
    df['AroonIndicator'] = ta.trend.aroon_down(df['Close'])
    df['AroonUp'] = ta.trend.aroon_up(df['Close'])
    df['CCI'] = ta.trend.cci(df['High'], df['Low'], df['Close'])
    df['DPO'] = ta.trend.dpo(df['Close'])
    df['EMA'] = ta.trend.ema_indicator(df['Close'])
    df['Ichimoku_A'] = ta.trend.ichimoku_a(df['High'], df['Low'])
    df['Ichimoku_B'] = ta.trend.ichimoku_b(df['High'], df['Low'])
    df['KST'] = ta.trend.kst(df['Close'])
    df['KSTSignal'] = ta.trend.kst_sig(df['Close'])
    df['MACD'] = ta.trend.macd(df['Close'])
    df['MACDDiff'] = ta.trend.macd_diff(df['Close'])
    df['MACDSignal'] = ta.trend.macd_signal(df['Close'])
    df['MassIndex'] = ta.trend.mass_index(df['High'], df['Low'])
    df['PSAR_Down'] = ta.trend.psar_down(df['High'], df['Low'], df['Close'])
    df['PSAR_DownIndicator'] = ta.trend.psar_down_indicator(df['High'], df['Low'], df['Close'])
    df['PSAR_Up'] = ta.trend.psar_up(df['High'], df['Low'], df['Close'])
    df['PSAR_UpIndicator'] = ta.trend.psar_up_indicator(df['High'], df['Low'], df['Close'])
    df['TRIX'] = ta.trend.trix(df['Close'])
    df['VortexIndicatorNeg'] = ta.trend.vortex_indicator_neg(df['High'], df['Low'], df['Close'])
    df['VortexIndicatorPos'] = ta.trend.vortex_indicator_pos(df['High'], df['Low'], df['Close'])
    df['CumulativeReturn'] = ta.others.cumulative_return(df['Close'])
    df['DailyLogReturn'] = ta.others.daily_log_return(df['Close'])
    df['DailyReturn'] = ta.others.daily_return(df['Close'])

    return df;


print("Loading Dataframe")

dateArr = START_DATE.split("-")

startDate = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]))
startDate = sub_business_days(startDate, PERIOD)

print("hi")
df = pdr.get_data_yahoo(STOCK, start=startDate)
print("Bie")

#df = pd.read_csv(CSV)
"""
#Trim dates
dropList = []
if START_DATE != '0':
    index = 0
    while df.iloc[index]['Date'] != START_DATE:
        #print(index, "| ", df.iloc[index]['Date'])
        dropList.append(index)
        index += 1
df = df.drop(dropList).reset_index()
"""
INITIALDF = copy.copy(df)
#print(len(df.index))
print("Populating Dataframe")
df = populateDataframe(df)
df = df.reset_index()
print("Calculating Labels from Target Period")
for i in range(len(df)):
    if i + TARGET_PERIOD >= df.shape[0]:
        break
    ## Compare to between close price and the targets close rpice
    #difference = df.iloc[i + PERIOD].Close - df.iloc[i].Close

    #For one day do difference in open and Close
    #difference = df.iloc[i+TARGET_PERIOD].Close - df.iloc[i].Close
    difference = df.iloc[i+TARGET_PERIOD].Close - df.iloc[i+1].Open

    #Can do binary here or regression
    #if(difference > 0):
    df.loc[i, 'Label'] = difference

    #print(difference)

#df.to_csv("TmpDataframe.csv", sep='\t')

dateDf = df['Date']

#df = df.drop(['Date'], axis=1)
df = df.fillna(0)
df.head()
#print(df.columns)
df = df.drop(['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'], axis=1)

# ## Clean Data

labels = df["Label"]

"""
High = df["High"]
Low = df["Low"]
Open = df["Open"]
Close = df["Close"]
Volume = df["Volume"]
AdjClose = df["Adj Close"]
"""

#Normalize the Data
dforiginal = df
x = df.values
scaler = preprocessing.MinMaxScaler()
xScaled = scaler.fit_transform(x)
df = pd.DataFrame(xScaled)
df.columns = dforiginal.columns
#df.head()

"""
# Dimensionality Reduction
PCA_COMPONENTS = 8

pca = PCA(n_components=PCA_COMPONENTS)
pca.fit(df)
df = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(PCA_COMPONENTS)], index=df.index)
"""

df["Labels"] = labels

"""
df["High"] = High
df["Low"] = Low
df["Open"] = Open
df["Close"] = Close
df["Volume"] = Volume
df["Adj Close"] = AdjClose
"""

dataArray = df.to_numpy()


INITIALINVEST = 5000

currentMoney = INITIALINVEST

tracker = []
for i in range(TARGET_PERIOD):
    tracker.append({
                    "Shares": 0,
                    "Profit": 0,
                    "BuyPrice": 0,
                    "BuyInvestment": 0,
                    "Buy": False,
                    })

print("Entering Program")
start = 0;
end = start + PERIOD;

dayCnt = 0
# In[72]:
profit = 0
wins = 0
losses = 0

#print(df)
#print(len(df))
#print(df.shape)
#print(start)
#print(end)

TruePos = 0
TrueNeg = 0
FalsePos = 0
FalseNeg = 0

while end + 1 + TARGET_PERIOD < df.shape[0]:

    targetAtts = dataArray[end,:-1]
    targetAtts = targetAtts.reshape(1, -1)
    targetLabel = dataArray[end,-1]

    xTrain = dataArray[start:end - 1,:-1]
    yTrain = dataArray[start:end -1,-1]

    #print(targetAtts.shape)
    #print(targetLabel.shape)
    #print(xTrain.shape)
    #sprint(yTrain.shape)

    CROSS_VAL = 10
    predSum = 0
    for i in range(CROSS_VAL):
        model = MLPRegressor(solver = 'adam', activation = 'relu', hidden_layer_sizes = [128,128,128, 128], max_iter=1000)
        model.fit(xTrain, yTrain)
        predSingle = model.predict(targetAtts)[0]
        predSum += predSingle
    pred = predSum/CROSS_VAL

    """
    model = MLPRegressor(solver = 'adam', activation = 'relu', hidden_layer_sizes = [128,128,128, 128], max_iter=1000)
    model.fit(xTrain, yTrain)
    pred = model.predict(targetAtts)[0]
    """

    #Do something with percentage here
    print(dateDf.iloc[end], "------------------------")
    print(pred, " | ", targetLabel)
    if pred > 0 and targetLabel > 0:
        TruePos += 1
    elif pred > 0 and targetLabel <0:
        TrueNeg += 1
    elif pred < 0 and targetLabel > 0:
        FalsePos += 1
    elif pred < 0 and targetLabel < 0:
        FalseNeg += 1

    print("TruePos: ", TruePos)
    print("TrueNeg: ", TrueNeg)
    print("FalsePos: ", FalsePos)
    print("FalseNeg: ", FalseNeg)

    if pred >= 0:
        sharePrice = INITIALDF.iloc[end+1]['Open']
        sharesToBuy = math.floor((currentMoney/2)/sharePrice)
        currentMoney -= sharePrice * sharesToBuy
        print("\tBuying", sharesToBuy, "Shares at", sharePrice)
        tracker.append({
                        "Shares": sharesToBuy,
                        "Profit": targetLabel,
                        "BuyPrice": sharePrice,
                        "BuyInvestment": sharePrice * sharesToBuy,
                        "Buy": True,
                        })
    else:
        tracker.append({
                        "Shares": 0,
                        "Profit": 0,
                        "BuyPrice": 0,
                        "BuyInvestment": 0,
                        "Buy": False,
                        })

    if tracker[dayCnt].get("Buy") == True:
        tradeProfit = tracker[dayCnt].get("Profit") * tracker[dayCnt].get("Shares")
        #print(tracker[dayCnt].get("Profit"), " | ", INITIALDF.iloc[end]["Close"] - tracker[dayCnt].get("BuyPrice"))

        profit += tradeProfit
        currentMoney += tracker[dayCnt].get("BuyInvestment") + tradeProfit
        print("\nSelling", tracker[dayCnt].get("Shares"), "Shares")
        print("Bought at:", tracker[dayCnt].get("BuyPrice"), " Sold at:", INITIALDF.iloc[end]["Close"])
        print("Trade Profit:", tradeProfit, "\n")
        if tracker[start].get("Profit") > 0:
            print("WIN!")
            wins += 1
        else:
            print("Loss :(")
            losses += 1
        print("\tCurrent Money", currentMoney)
        print("\tCurrent Cumulative Profit:" , profit)
        print("\tWins: ", wins, " | Losses:", losses)
        print("\tWin Percentage:", wins/ (losses + wins))
        print("\tReturn:", currentMoney/INITIALINVEST)
        print("\tDays Elapsed:", dayCnt)
        print("\n")
    dayCnt += 1
    start += 1
    end += 1

while dayCnt < len(tracker):

    print( dateDf.iloc[end], "------------------------")
    if tracker[dayCnt].get("Buy") == True:
        tradeProfit = tracker[dayCnt].get("Profit") * tracker[dayCnt].get("Shares")
        #print(tracker[dayCnt].get("Profit"), " | ", INITIALDF.iloc[end]["Close"] - tracker[dayCnt].get("BuyPrice"))
        profit += tradeProfit
        currentMoney += tracker[dayCnt].get("BuyInvestment") + tradeProfit
        print("\nSelling", tracker[dayCnt].get("Shares"), "Shares")
        print("Bought at:", tracker[dayCnt].get("BuyPrice"), " Sold at:", INITIALDF.iloc[end]["Close"])
        print("Trade Profit:", tradeProfit, "\n")
        if tracker[start].get("Profit") > 0:
            print("WIN!")
            wins += 1
        else:
            print("Loss :(")
            losses += 1
        print("\tCurrent Money:", currentMoney)
        print("\tCurrent Cumulative Profit:" , profit)
        print("\tWins: ", wins, " | Losses:", losses)
        print("\tWin Percentage:", wins/ (losses + wins))
        print("\tReturn:", currentMoney/INITIALINVEST)
        print("\tDays Elapsed:", dayCnt)
        print("\n")
    dayCnt += 1
    start+=1
    end += 1

print("\nSummary:")
print("\tTotal Money:", currentMoney)
print("\tCumulative  Profit:" , profit)
print("\tWins: ", wins, " | Losses:", losses)
print("\tWin Percentage:", wins/ (losses + wins))
print("\tReturn:", currentMoney/INITIALINVEST)
print("\tDays Elapsed:", dayCnt)
