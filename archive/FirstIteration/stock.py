#from yahoo_fin import stock_info as si
from Robinhood import Robinhood
from bs4 import BeautifulSoup
import sys
import requests
import datetime
import math
from pytz import timezone
tz = timezone('EST')

import ta

#Stock Class
class Stock:

    # Class Variables
    askPrice = 0
    askSize = 0
    bidPrice = 0
    bidSize = 0
    initial = 0
    highPoint = 0
    profit = 0
    sellPrice = None
    capital = 0

    #TODO Technical Analysis


    """
    Initialize class
    """
    # Initialize name on creation
    def __init__(self, trader, name, investPer, capital):
        quote = trader.quote_data(name)
        self.name = name
        self.askPrice = float(quote['ask_price'])
        self.askSize = float(quote['ask_size'])
        self.bidPrice = float(quote['bid_price'])
        self.bidSize = float(quote['bid_size'])
        self.numShares = math.floor(investPer/self.bidPrice)
        self.initial = float(quote['ask_price'])
        self.highPoint = float(quote['bid_price'])
        self.capital = capital

        #TODO Buy on initialization?

        #TODO Initialize time series csv

    def update(self, trader):
        quote = trader.quote_data(self.name)
        self.askPrice = float(quote['ask_price'])
        self.askSize = float(quote['ask_size'])
        self.bidPrice = float(quote['bid_price'])
        self.bidSize = float(quote['bid_size'])
        if self.highPoint < float(quote['bid_price']):
            self.highPoint = float(quote['bid_price'])

        # TODO
        # Implement analysis on time series
        # Implement previous day data to start day.


    """
    Decides whether to sell of stocks.
    Sell if decreases more than 20%
    Sell if gain of more than 100% from intial investment
    """
    def checkTrade(self, trader, decreaseSell, increaseSell, printOutput, f):


        investment = self.initial * self.numShares
        sellReturn = self.bidPrice * self.numShares

        curReturn = investment - sellReturn

        if curReturn < 0:
            if math.fabs(curReturn) > self.capital * .01:
                #Sell
                sell(trader, stock)
                self.sellPrice = self.bidPrice
        else:
            if curReturn > self.capital * .25:
                sell(trader, stock)
                self.sellPrice = self.bidPrice

        """
        changeHigh = ((self.bidPrice - self.highPoint)/self.highPoint)
        changeInitial = ((self.bidPrice - self.initial)/self.initial)

        #Stock Increased
        if changeHigh >= 0:
            if increaseSell != None and changeInitial > increaseSell:

                #TODO Sell
                string = "Pulling out of " + stock
                printStr(string, printOutput, f)

                sell(trader, stock)
                self.sellPrice = self.bidPrice
                self.highPoint = self.bidPrice
            else:
                self.highPoint = self.bidPrice

        #Stock Decreased
        else:

            #Convert percent decrease to positive number
            percentChange = math.fabs(percentChange)

            #Check if stock decreased over limit
            if percentChange > decreaseSell:
                #Sell
                if printOutput:
                    print("Pulling out of",stock)
                else:
                    print("Pulling out of",stock, file=f)
                    f.flush()

                #TODO Sell
                sell(trader, stock)
                self.sellPrice = self.bidPrice
        """
        return self


    """
    Pull out of stock
    """
    def pullOut(self, trader):
        #Check if stock has been sold already
        if self.sellPrice == None:
            #TODO Sell
            self.sell(trader)
            self.sellPrice = self.bidPrice

    """
    Buy a stock
    """
    def buy(self, trader, numStocks):
        return 1

    """
    Sell a stock
    """
    def sell(self, trader, numStocks = None):
        return 1

    """
    Calulcates profit of stock
    """
    def getProfit(self):
        #Stock was already sold
        if self.sellPrice != None:

            #Calculate profit and print
            stockProfit = self.sellPrice - self.initial

        #Stock has not been sold yet
        else:
            #Calculate hypothetical profit and print
            stockProfit = self.bidPrice - self.initial
            self.profit = stockProfit
        return stockProfit

    """
    Print information on stock. Works with the print all stocks function
    """
    def printStock(self, printOutput, f):

        if printOutput:
            print("{:5s} {:1s} {:9s}  {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:12s} {:1s} {:12s}".format(
            self.name, "|", str(self.askPrice)[:10], "|", str(self.askSize), "|", str(self.bidPrice)[:10], "|", str(self.bidSize), "|", str(self.initial)[:10],
            "|", str(self.highPoint)[:10], "|", str(self.numShares), "|", str(self.sellPrice)[:10], "|", str(self.profit)[:8]))
        else:
            print("{:5s} {:1s} {:9s}  {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:12s} {:1s} {:12s}".format(
            self.name, "|", str(self.askPrice)[:10], "|", str(self.askSize), "|", str(self.bidPrice)[:10], "|", str(self.bidSize), "|", str(self.initial)[:10],
            "|", str(self.highPoint)[:10], "|", str(self.numShares), "|", str(self.sellPrice)[:10], "|", str(self.profit)[:8]), file = f)

