"""
 * File Name: run.py
 * Author: Bernard Suwirjo
 *
 * Runs a trading algorithm throughout the day.
 *
 * The program scrapes a website for the top trending stocks and then invests in them.
 * The program will then watch those stocks throughout the day and sell if the bid price goes below
 * a certin threshold. The program buys only once a day and sells throughout. The program sells all
 * stocks that it has not sold at the end of every day. 4:30pm EST.
"""

from Robinhood import Robinhood # Robinhood api to check/buy/sell stocks
#from bs4 import BeautifulSoup # Webscraper
#import requests
import datetime # Getting current time
import sys
#import math # math.floor, making sure we don't overbuy stocks
from pytz import timezone # Change timezone to est
tz = timezone('EST')

#Import helper methods
from stockMethods import *



#Variables
capital, numInvest, decreaseSell, increaseSell, url, printOutput, f = processCmdin(sys.argv)

#Log Start of Program
if printOutput:
    print("Starting program\n")
else:
    print("Starting program\n", file=f)

fileName = open("../cred", "r")
contents = fileName.read()
user = contents.split()[0]
pwd = contents.split()[1]
fileName.close

#Log into Robinhood
trader = Robinhood()
login = trader.login(username=user, password=pwd)
if login == True:
    string = "Login Successful\n"
    printStr(string, printOutput, f)
else:
    string = "Login Failed, Exiting"
    printStr(string, printOutput, f)
    sys.exit()


# Initialize, scrape data, invest in top 10 stocks
investPer = capital/float(numInvest)
stocks = initialize(numInvest, url, trader, investPer, capital, printOutput, f)

#Print Start of trading loop
time = getTime()
string = '\nStarting Trading Loop at ' + time +  '\n'
printStr(string, printOutput, f)

#Loop and update until 4:00pm or until we've sold all our stocks
while True:

    #End loop and pull out 4:00pm
    currentTime = datetime.datetime.now(tz)
    if currentTime.hour >= 30:
        break

    if haveStock(stocks):
        break
    #Update Stocks, Check if should Trade, and calculate potential profit after
    stocks = updateAll(trader, stocks)
    stocks = checkTrades(trader, stocks, decreaseSell, increaseSell, printOutput, f)
    potentialProfit, profit = totalProfit(stocks)

    #Print Stocks
    printStocks(stocks, printOutput, f)

#Pull out and calculate end profit
stocks = pullOutAll(trader, stocks)
endProfit, profits = totalProfit(stocks)

#Print end profits for the day
currentTime = datetime.datetime.now(tz)
date = str(currentTime.month) + "/" + str(currentTime.day) + "/" + str(currentTime.year)
string = "End Profit for " + date + " is " + str(endProfit)
printStr(string, printOutput, f)
