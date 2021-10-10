from database import Crypto, Database
from flask import Flask, render_template, redirect
from flask import request
from apicoin import ApiCoinMarkt as api
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def acceuil():
    load_dotenv("./app.env")
    db = Database()
    coin = api(db)
    coin.get_quote()
    #coin.get_plot_by_id(1)
    crypto_list = db.get_all_crypto_full()
    prices=[]
    for crypto in crypto_list :
        prices.append(crypto.price)
    prices=sum(prices)
    return render_template('accueil.html',cryptos=crypto_list,prices=prices)
        
    #load_dotenv("./app.env")
    #db = Database()
    #a = api(db)
    #a.get_quote()
    #a.get_plot_by_name('ETH')

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
    load_dotenv("./app.env")
    db = Database()

    if request.method == 'GET': 
        crypto_list = db.get_all_crypto_labels()
        return render_template('edit.html', cryptomonais=crypto_list)

    if request.method == 'POST':
        form = request.form
        price = form.get('price')
        many = form.get('quantity')
        cash = form.get('cash')

        db.insert_crypto(Crypto(cash,price,many))
        return redirect("/", code=200)

@app.route("/modify/<id>", methods = ['GET', 'POST', 'DELETE'])
def modify(id):
    load_dotenv("./app.env")
    db = Database()

    if request.method == 'GET': 
        crypto_list = db.get_all_crypto_labels()
        crypto = db.get_crypto_by_id(id)
        print(crypto)
        return render_template('modify.html', cryptomonais=crypto_list, currentcrypto=crypto)

    if request.method == 'POST':
        form = request.form
        id_crypto = form.get('id_crypto')
        price = form.get('price')
        many = form.get('quantity')

        db.modify_crypto(id=id,id_crypto=id_crypto,price=price,many=many)
        return redirect("/", code=200)

    if request.method == 'DELETE':
        print(id)
        db.remove_crypto(id)
        return redirect("/", code=200)