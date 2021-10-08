from database import Crypto, Database
from flask import Flask, render_template
from apicoin import ApiCoinMarkt as api
from dotenv import load_dotenv


#if __name__ == "__main__":
    #load_dotenv("./app.env")
    #db = Database()
    #crypto_list = db.get_all_crypto_full()
    #li = db.get_all_crypto()
    #for i in li :
    #    print(i)
    #a = api(db)
    #a.get_quote()
    #a.get_plot_by_name('ETH')
app = Flask(__name__)

@app.route("/")
def hello_world():
    load_dotenv("./app.env")
    db = Database()
    crypto_list = db.get_all_crypto_full()
    prices=[]
    for crypto in crypto_list :
        prices.append(crypto.price)
    return render_template('accueil.html',cryptos=crypto_list,prices=sum(prices))
        
    #load_dotenv("./app.env")
    #db = Database()
    #a = api(db)
    #a.get_quote()
    #a.get_plot_by_name('ETH')
