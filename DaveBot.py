# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import santa_shares
import json
import pandas as pd
import time

# instanciate the user & shop
myUser = santa_shares.User('https://santa-shares.azurewebsites.net','DaveBot')
myShop = santa_shares.Shop('https://santa-shares.azurewebsites.net')

# register the user
myUser.register()

print(myUser.token)
print(myUser.get_status())


# get the shop items
allItems = myShop.get_items()

#dump to file:
with open("items_file.json", "w") as write_file:
    json.dump(allItems, write_file)

#order the list:
# Create DataFrame
df = pd.DataFrame(allItems)

#print(df['item_id']>0)

# making boolean series for a team name 
print("filtering by amount")
filter = df["amount"]>0
#print(filter)


print("getting sorted list")
df_available = df[ (df[["amount"]]>0).all(axis=1) ]
# sort by price
df_sorted = df_available.sort_values(by=['price'])

# filtering data 
print("cleaning data")
df_clean = df_sorted.dropna()

   
#for i in range(0,10):
#    myUser.buy(114,1)
#    myUser.sell(114,1)
#    time.sleep(2)

print("outputting the list")
#for label, content in df_clean.items():
#   print(content)
print(df_clean)
    
for row in df_clean.itertuples():
    print(row.item_name + " is price " +  str(row.price) + " with amount " + str(row.amount))

# buy ALL THE CHEAP THINGS
for row in df_clean.itertuples():
    myUser.buy(row.item_id,row.amount)

print(myUser.get_status())

