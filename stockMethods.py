"""
 * File Name: getRemainder.s
 * Author: Bernard Suwirjo
 *
 * Helper functions for main training program.
 *
 * processCmdin(argv) - capital, numInvest, decreaseSell, increaseSell, url, printOutput, f
 * initialize(n, url) - None
 * update(trader, stockNames, stocks) - stocks
 * checkTrade(trader, stockNames, stocks, decreaseSell, increaseSell = None) - stocks
 * profit(stockNames, stocks) - totalProfit, profits
 * pullOut(trader, stockNames, stocks) - stocks
 * buyStock(trader, stock, numStocks)
 * sellStock(trader, numStocks = None)
 * printStocks(stockNames, stocks)
 * getTime() - time
 *
"""

#from yahoo_fin import stock_info as si
from Robinhood import Robinhood
from bs4 import BeautifulSoup
import sys
import requests
import datetime
import math
from pytz import timezone
tz = timezone('EST')

from stock import *

"""
Proccesses command line input
Returns, variables processed from command line inputs.
"""
def processCmdin(argv):
    if len(argv) != 5:
        print(len(argv))
        print("Error with command line inputs")
        sys.exit(0)
    else:
        capital = int(argv[1]) # Dollar amount intial investment
        numInvest = int(argv[2]) # Number of stocks to invest in
        stockType = int(argv[5]) # 0-regular stocks, 1-penny stocks
        printOutput = int(argv[6]) # 0-file output, 1-print output


    #URL's for penny and regular stocks
    regularUrl = "https://stock-screener.org/trending-stocks.aspx"
    pennyUrl = "https://stock-screener.org/penny-stock-screener.aspx"

    #Check stock type is in bounds and set url
    if stockType == 0:
        url = regularUrl
    elif stockType == 1:
        url = pennyUrl
    else:
        print("Error with stock type, argument 6 ,exiting program")
        sys.exit()

    #Check if there is an increase limit
    if increaseSell <= 0:
        increaseSell = None

    #Check output type is in bounds and convert to boolean
    printOutput
    if printOutput == 0:
        printOutput = False
    elif printOutput == 1:
        printOutput = True
    else:
        print("Error with output type, argument 7, exiting program")
        sys.exit()

    f = None
    # Set up writing output to file
    if printOutput ==  False:
        selfTime= datetime.datetime.now(tz)
        date = str(selfTime.month) + "_" + str(selfTime.day)

        directory = "logs/" + date
        if not os.path.exists(directory):
                os.makedirs(directory)
        if stockType == 0:
            fname = "logs/" + date + "/regular_" + date + ".txt"
        else:
            fname = "logs/" + date + "/penny_" + date + ".txt"

        f = open(fname, 'w+')

    return capital, numInvest, decreaseSell, increaseSell, url, printOutput, f


"""
Grabs top 10 stocks and initalizes name array and stock dictionary.
"""
def initialize(n, url, trader, investPer, capital, printOutput, f):

    stocks = {} #Dictionary to hold stocks and info

    string = "Scraping top " + str(n) + " stocks"
    printStr(string, printOutput, f)

    #Load webpage and grab top n stocks
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    html = soup.find('tbody')
    html = html.findAll('tr')

    cnt = 0

    for ele in html:
        if cnt >= n:
            break
        ticker = ele.find('td').text.split(' ')[1]

        stocks[ticker] = Stock(trader, ticker, investPer, capital)

        current = stocks[ticker]
        string = "Investing " + str(current.numShares * current.initial) + " dollars in " + current.name + " at " + str(current.initial) + " for " +  str(current.numShares) + " stocks"
        printStr(string, printOutput, f)
        stocks[ticker].initial = current.bidPrice
        stocks[ticker].buy(trader, current.numShares)

        cnt += 1

    return stocks

"""
Updates the quote data for every stock.
"""
def updateAll(trader, stocks):
    for key, stock in stocks.items():
        stock.update(trader)
    return stocks

def checkTrades(trader, stocks, decreaseSell, increaseSell, printOutput, f):
    for key, stock in stocks.items():
        stock = stock.checkTrade(trader, decreaseSell, increaseSell, printOutput, f)
    return stocks
"""
Checks either end profit or hypothetical profit if we were to sell all
"""
def totalProfit(stocks):
    profits = {}
    #Create a profit counter and iterate through all stocks
    totalProfit = 0
    for key, stock in stocks.items():
        current =  stock
        stockProfit = current.getProfit()
        totalProfit += stockProfit
        profits[stock] = stockProfit
    return totalProfit, profits


"""
Pull out of stock
"""
def pullOutAll( trader, stocks):
    for key, stock in stocks.items():
        stock.pullOut(trader)
    return stocks
"""
Checks if we have a bought stock
"""
def haveStock(stocks):
    have = False
    for key, stock in stocks.items():
        if stock.sellPrice != None:
            have  = True
    return have

"""
Prints String
"""
def printStr(string, printOutput, f):
    if printOutput:
        print(string)
    else:
        print(string, file = f)
        f.flush()

"""
Print quote data for each stock.

Stock | Ask Price | Ask Size | Bid Price | Bid Size | Bought at | Num Shares | Num Stocks| High | Sell | Profit|
"""
def printStocks(stocks, printOutput, f):

    #Print Stock Header

    string = "{:5s} {:1s} {:9s}  {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:10s} {:1s} {:12s} {:1s} {:12s} {:1s} {:12s} {:12s}".format(
        "Tick", "|", "Ask Price", "|", "Ask Size", "|", "Bid Price", "|", "Bid Size", "|", "Bought At",
        "|", "Day High",  "|", "Shares" ,"|",  "Sold At", "|", "Profit", getTime())
    printStr(string, printOutput, f)


    #Print data from stocks
    for key, stock in stocks.items():
        stock.printStock(printOutput, f)

    totalProfits, profits = totalProfit(stocks)
    string = "Total Profits: " + str(totalProfits) + "\n"
    printStr(string, printOutput, f)

"""
Returns time in hour:minute format
"""
def getTime():
    selfTime= datetime.datetime.now(tz)
    time = str(selfTime.hour) + ":" + str(selfTime.minute)
    return time
