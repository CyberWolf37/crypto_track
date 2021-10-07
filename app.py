from database import Crypto, Database
from flask import Flask, render_template
from apicoin import ApiCoinMarkt as api
from dotenv import load_dotenv


#if __name__ == "__main__":
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('accueil.html')
        
    #load_dotenv("./app.env")
    #db = Database()
    #a = api(db)
    #a.get_quote()
    #a.get_plot_by_name('ETH')
