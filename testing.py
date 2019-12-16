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
myUser = santa_shares.User('https://santa-shares.azurewebsites.net','DavidBot')
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

#myStuff = pd.array([])
myStuff = pd.DataFrame({'item_id' : [], 'price_bought' : []})

# buy ALL THE CHEAP THINGS
for row in df_clean.itertuples():
    myUser.buy(row.item_id,row.amount)
    myStuff.append({'item_id': row.item_id, 'price_bought': df_clean([row,'price'])})

print(myUser.get_status())

transaction_fee = 50

iter = 0

while iter:
    # get prices as dataframe
    all_curr_prices = santa_shares.get_curr_prices()
    for i in row.item_id:
        curr_price = all_curr_prices[i]
        sale_price_now = myStuff[i,'price']
        if (sale_price_now - curr_price - transaction_fee)>0:
            #then sell all for profit
            myUser.sell(row.item_id,1000)
            #todo - need to check if that sells OK!!!
        
        moreStuff = santa_shares.buy_cheap_stuff(myUser,df_clean,myStuff)
        # then add this to the list of stuff
        myStuff.append(moreStuff)
    
    print(myUser.get_status())
    
    time.sleep(30)


