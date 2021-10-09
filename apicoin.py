import requests
from database import Database, Crypto_quote
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import os 
from  dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class ApiCoinMarkt() :

    def __init__(self,database:Database):
        self.key = os.environ.get("KEY_MARKET_CAP")
        self.url = os.environ.get("URL")
        self.db = database
        

    def get_quote(self) :
        delta = datetime.now() - datetime.strptime(self.db.get_last_date(),'%Y-%m-%d %H:%M:%S.%f')
        if delta.days > 1 :
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
                filter_data = [x for x in data['data'] if x['symbol'] in list_crypto]
                for i in filter_data:
                    name = i['symbol']
                    price = i['quote']['EUR']['price']
                    when = datetime.now()

                    print(name +" "+price++" "+when)

                    cryo = Crypto_quote(name=name,price=price,when=when)
                    self.db.insert_crypto_quote(cryo)
                
                
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print(e)

    def get_plot_by_name(self,name) :
        fig = plt.figure(figsize = (18,8))
        prices = self.db.get_all_crypto_price_by_name(name)
        print(prices)
        plt.plot(data=prices)
        html = mpld3.fig_to_html(fig)
        print(html)
        #print(prices)
        #plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
        #plot = plt.plot(prices,ylabel='Prix',xlabel='Date')

        #return plot