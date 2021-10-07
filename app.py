from database import Crypto, Database
from apicoin import ApiCoinMarkt as api
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv("./app.env")
    db = Database()
    a = api(db)
    a.get_quote()
    #a.get_plot_by_name('ETH')
