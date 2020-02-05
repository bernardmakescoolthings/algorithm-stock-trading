from Robinhood import Robinhood # Robinhood api to check/buy/sell stocks
#from bs4 import BeautifulSoup # Webscraper
#import requests
import datetime # Getting current time
import sys
#import math # math.floor, making sure we don't overbuy stocks
from pytz import timezone # Change timezone to est
tz = timezone('EST')


fileName = open("../cred", "r")
contents = fileName.read()
user = contents.split()[0]
pwd = contents.split()[1]
fileName.close

print(user)
print(pwd)

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
