from database import Crypto, Database
from apicoin import ApiCoinMarkt as api


if __name__ == "__main__":
    a = api()
    a.get_quote()
