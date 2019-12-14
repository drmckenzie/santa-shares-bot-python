# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import santa_shares
import json
import pandas as pd

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
filter = df["amount"]>0
  
# filtering data 
df.where(filter, inplace = True)

print(df.dropna())

print(df)
   
myUser.buy(1,1)

print(myUser.get_status())

