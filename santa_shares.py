import os, requests, json
import sys
import pandas as pd

class Shop:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_items(self):
        return requests.get(f"{self.api_url}/api/items").json()

    def get_item(self, item_id):
        return requests.get(f"{self.api_url}/api/items/{item_id}").json()

class User:
    def __init__(self, api_url, user_name):
        self.user_name = user_name
        self.config_file_name = f"{user_name}.json"
        self.api_url = api_url
        self.token = None
        print("Initialsied correctly")

    def register(self):
        print("inside register")
        if not os.path.exists(self.config_file_name):
            response = requests.post(self.api_url+"/api/users", json={ "user_name" : self.user_name })
            if response.status_code != 201:
                print(f"[{response.status_code}]")
                sys.exit()
            else:
                print("registering...")
                json_response = response.json()
                self.user_id = json_response.get("user_id")
                self.token = json_response.get("token")
                with open(self.config_file_name, "w") as file:
                    json.dump({
                        "user_id" : self.user_id,
                        "user_name" : self.user_name,
                        "token" : self.token,
                    }, file)

        with open(self.config_file_name, "r") as file:
            json_data = json.load(file)
            self.user_id = json_data["user_id"]
            self.user_name = json_data["user_name"]
            self.token = json_data["token"]

        self.headers = { "Authorization" : f"token {self.token}" }

    def get_status(self):
        return requests.get(f"{self.api_url}/api/users/{self.user_id}", headers=self.headers).json()

    def buy(self, item_id, amount):
        return requests.post(f"{self.api_url}/api/buy", headers=self.headers, json={ "item_id" : item_id, "amount" : amount })
        #if response.status != 201: print(f"[{response.status}] [{response.message}]")

    def sell(self, item_id, amount):
        return requests.post(f"{self.api_url}/api/sell", headers=self.headers, json={ "item_id" : item_id, "amount" : amount })
        #if response.status != 201: print(f"[{response.status}] [{response.message}]")
        
    def get_prices(self):
        # get the shop items
        allItems = myShop.get_items()

        #order the list:
        # Create DataFrame
        df = pd.DataFrame(allItems)

        # sort by price
        df_sorted = df.sort_values(by=['price'])
        return df_sorted
    
    def buy_cheap_stuff(self,myUser,df,myStuff):
        #myStuff = pd.DataFrame({'item_id' : [], 'price_bought' : []})

        # buy ALL THE CHEAP THINGS
        for row in df.itertuples():
            myUser.buy(row.item_id,row.amount)
            myStuff.append({'item_id': row.item_id, 'price_bought': df([item_id,'price'])})
