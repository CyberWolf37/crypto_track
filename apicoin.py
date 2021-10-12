import requests
from database import Database, Crypto_quote
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
                    id = self.db.get_id_by_symbol(i['symbol'])
                    price = i['quote']['EUR']['price']
                    when = datetime.now()

                    cryo = Crypto_quote(id=id,price=price,when=when)
                    self.db.insert_crypto_quote(cryo)
                
                
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print(e)

    def get_plot_by_id(self,id) :

        # get price by id and date
        print('id =',id)
        prices = self.db.get_all_price_by_id(id)
        dates = self.db.get_all_date_by_id(id)
        print(dates)
        dates = [datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f') for i in dates]
        cryo = self.db.get_crypto_by_id(id)

        fig = plt.figure(figsize=(4,2))
        plt.plot_date(dates,prices,label='prix du marché',c='b')
        plt.plot()
        plt.legend()
        plt.xlim(dates)
        plt.axhline(y=4,c='g',label='Prix acheté')
        plt.ylabel('Price')
        plt.xlabel('dates')
        plt.legend()
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
        plt.gca().xaxis.set_major_formatter(myFmt)
        html = mpld3.fig_to_html(fig)
        return html