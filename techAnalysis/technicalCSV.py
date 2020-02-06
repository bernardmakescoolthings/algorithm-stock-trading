from Robinhood import Robinhood # Robinhood api to check/buy/sell stocks
#from bs4 import BeautifulSoup # Webscraper
#import requests
import datetime # Getting current time
import sys
#import math # math.floor, making sure we don't overbuy stocks
from pytz import timezone # Change timezone to est
tz = timezone('EST')

from datetime import datetime, timedelta

import yfinance as yf
import ta
import numpy as np

import pandas as pd
from pandas_datareader import data as pdr
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.decomposition import PCA

#Supress Warnings
import warnings
warnings.filterwarnings("ignore")

TARGET_PERIOD=1
#PERIOD = 100

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
    #df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
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
    #df['ADXNeg'] = ta.trend.adx_neg(df['High'], df['Low'], df['Close'])
    #df['ADXPos'] = ta.trend.adx_pos(df['High'], df['Low'], df['Close'])
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


"""
fileName = open("/home/bsuwirjo/cred", "r")
contents = fileName.read()
user = contents.split()[0]
pwd = contents.split()[1]
fileName.close

print(user)
#print(pwd)

#Log into Robinhood
trader = Robinhood()
login = trader.login(username=user, password=pwd)
if login == True:
    string = "Login Successful\n"
    print(string)
else:
    string = "Login Failed, Exiting"
    print(string)
    sys.exit()
"""

periodArr = [100, 150, 200, 250]

stockFile = open("stocks.txt", "r")
for stock in stockFile:
    stock = stock.split()[0]

    for PERIOD in periodArr:

        dateObj = datetime.now() - timedelta(days=1)
        dateStartObj = datetime.now() - timedelta(days=PERIOD)

        dateEnd = str(dateObj.year) + "-" + str(dateObj.month) + "-"+ str(dateObj.day)
        dateStart = str(dateStartObj.year) + "-" + str(dateStartObj.month) + "-"+ str(dateStartObj.day)

        df = pdr.get_data_yahoo(stock, start=dateStart, end=dateEnd)
        #print(df.head())
        #print(df)

        df = populateDataframe(df)
        df = df.reset_index()

        for i in range(len(df)):
            if i + TARGET_PERIOD >= df.shape[0]:
                break
            ## Compare to between close price and the targets close rpice
            #difference = df.iloc[i + PERIOD].Close - df.iloc[i].Close

            #For one day do difference in open and Close
            difference = df.iloc[i+TARGET_PERIOD].Close - df.iloc[i].Close
            #print(difference)
            #Can do binary here or regression
            #if(difference > 0):
            df.loc[i, 'Label'] = difference

            #print(difference)

        dateDf = df['Date']
        #df = df.drop(['Date'], axis=1)
        df = df.drop(['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'], axis=1)
        df = df.fillna(0)



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

        """
        # Dimensionality Reduction
        PCA_COMPONENTS = 8

        pca = PCA(n_components=PCA_COMPONENTS)
        pca.fit(df)
        df = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(PCA_COMPONENTS)], index=df.index)
        """

        #df.drop(df.tail(TARGET_PERIOD).index,inplace=True)

        df["Label"] = labels
        date = dateDf[len(dateDf)-1]



        dataArray = df.to_numpy()
        #targetAtts = targetAtts.to_numpy()


        targetAtts = dataArray[dataArray.shape[0]-TARGET_PERIOD,:-1]
        targetAtts = targetAtts.reshape(1, -1)
        xTrain = dataArray[:dataArray.shape[0]-TARGET_PERIOD,:-1]
        yTrain = dataArray[:dataArray.shape[0]-TARGET_PERIOD,-1]

        #print(targetAtts.shape)
        #print(targetLabel.shape)
        #print(xTrain.shape)
        #sprint(yTrain.shape)

        #print(targetAtts)
        #print(xTrain[len(xTrain)-1])

        model = MLPRegressor(solver = 'adam', activation = 'relu', hidden_layer_sizes = [128, 128, 128, 128])
        model.fit(xTrain, yTrain)
        pred = model.predict(targetAtts)[0]
        print(date, " | ", stock, " | ", PERIOD, " | ", pred)
    print("\n")
