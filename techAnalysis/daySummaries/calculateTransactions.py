import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Error with command line arguments")
    sys.exit()
else:
    DATE = sys.argv[1] #MONTH/DAY/YEAR
data = pd.read_csv('transactions.csv')

stockDict = {};

"""
stockTemplate = {
      "Stock": ""
      "BuyPrice": 0,
      "SellPrice": 0,
      "Quantity": 0,
      "Profit": 0,
      "ProfitPercentage": 0,
}
"""

#print(data.columns)

#GET COLUMN
#print(data["SYMBOL"])

#Get Row
#print(data.iloc[2])


#Populate Stock Dictionary
for index, row in data.iterrows():
    if row["DATE"] != DATE:
        continue
    #print(row)

    if row["DESCRIPTION"].split()[0] == "Bought":
        stockDict[row["SYMBOL"]] =  {
              "BuyPrice": 0,
              "SellPrice": 0,
              "Quantity": 0,
              "Profit": 0,
              "ProfitPercentage": 0,
        }
        stockObj = stockDict[row["SYMBOL"]]
        stockObj["BuyPrice"] = row["PRICE"]
        stockObj["Quantity"] = row["QUANTITY"]

    elif row["DESCRIPTION"].split()[0] == "Sold":
        stockObj = stockDict[row["SYMBOL"]]
        stockObj["SellPrice"] = row["PRICE"]

    #else:
        #print("There was an error fix it")

print("Stock Specifics:")
for key, value in stockDict.items():
    bought = value["BuyPrice"]
    sold = value["SellPrice"]
    profit = (sold - bought) * value["Quantity"]
    profitPercentage = (sold - bought)/bought * 100
    stockDict[key]["Profit"] = profit
    stockDict[key]["ProfitPercentage"] = profitPercentage
    print(key, "| Profit: ", profit, "| Profit Percentage: ", profitPercentage, "\n")


profitActual = 0
profitPercentage = 0
totalSpent = 0
for key, value in stockDict.items():
    profitActual += value["Profit"]
    profitPercentage += value["ProfitPercentage"]
    totalSpent += value["BuyPrice"]

print("Day Summary")
print("Total Spent", totalSpent)
print("Total Profit: ", profitActual)
print("Total Profit Percentage: ", profitPercentage)
print("Percent Return", profitActual/totalSpent * 100)
