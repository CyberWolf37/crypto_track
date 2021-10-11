import requests
import json
from database import Database, Crypto
from dotenv import load_dotenv

load_dotenv("./app.env")
url = 'http://127.0.0.1:5000/'
db = Database()

def test_home():
    r = requests.get(url)
    print("test_home : ",r.status_code)

def test_edit():
    r = requests.get(url + 'edit')
    print("test_edit : ",r.status_code)

def test_edit_post():
    data = {
        'cash': '2',
        'quantity': '2',
        'price': '300'
    }
    r = requests.post(url + 'edit',data=data)
    print("test_edit_post : ",r.status_code)

def test_modify():
    data = db.get_last_crypto()
    r = requests.get(url + 'modify/'+ str(data.id))
    print("test_modify : ",r.status_code)

def test_modify_post():
    data = {
        'id_crypto': '3',
        'quantity': '2.0',
        'price': '150000'
    }

    cryo = db.get_last_crypto()
    r = requests.get(url + 'modify/'+ str(cryo.id),data=data)
    print("test_modify_post : ",r.status_code)

def test_modify_delete():
    data = db.get_last_crypto()
    r = requests.delete(url + 'modify/'+ str(data.id))
    print("test_modify_delete : ",r.status_code)

if __name__ == "__main__":
    test_home()
    test_edit()
    test_edit_post()
    test_modify()
    test_modify_post()
    test_modify_delete()