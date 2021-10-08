import requests
from database import Database, Crypto_quote
from datetime import datetime
import matplotlib.pyplot as plt
import os 
from  dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class ApiCoinMarkt() :

    def __init__(self,database:Database):
        self.key = os.environ.get("KEY_MARKET_CAP")
        self.url = os.environ.get("url")
        self.db = database
        

    def get_quote(self) :
        parameters = {
        "start": "1",
        "limit": "100",
        "convert":"EUR",
        }
        headers = {
        "Accepts": "application/json",
        "Accept-Encoding": "deflate, gzip",
        "X-CMC_PRO_API_KEY": self.key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(self.url, params=parameters)
            data = json.loads(response.text)
            list_crypto = self.db.get_all_crypto_symbol()
            print(list_crypto)
            filter_data = [x for x in data['data'] if x['symbol'] in list_crypto]
            for i in filter_data:
                name = i['symbol']
                price = i['quote']['EUR']['price']
                when = datetime.now()

                cryo = Crypto_quote(name=name,price=price,when=when)
                self.db.insert_crypto_quote(cryo)
            
            
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def get_plot_by_name(self,name) :
        prices = self.db.get_all_crypto_price_by_name(name)
        print(prices)
        #plot = plt.plot(prices,ylabel='Prix',xlabel='Date')

        #return plot