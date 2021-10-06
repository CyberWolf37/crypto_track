import requests
import os
from  dotenv import load_dotenv
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class ApiCoinMarkt() :

    def __init__(self):
        load_dotenv("./app.env")
        self.key = os.environ.get("KEY_MARKET_CAP")
        self.url = os.environ.get("url")
        

    def get_quote(self, name=None) :
        print(self.url)
        parameters = {
        "start": "1",
        "limit": "100",
        "sort": "symbol=ETH",
        "convert":"EUR"
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
            print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)