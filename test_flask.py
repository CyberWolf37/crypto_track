import requests
import json
from database import Database, Crypto
from dotenv import load_dotenv

load_dotenv("./app.env")
db=Database()

def test_home():
    r = requests.get('http://127.0.0.1:5000/')
    print("test_home : ",r.status_code)

def test_edit():
    r = requests.get('http://127.0.0.1:5000/edit')
    print("test_edit : ",r.status_code)

def test_edit_post():
    data = {
        'cash': '2',
        'quantity': '2',
        'price': '300'
    }
    r = requests.post('http://127.0.0.1:5000/edit',data=data)
    print("test_edit_post : ",r.status_code)

def test_edit_delete():
    data = db.get_last_crypto()
    r = requests.delete('http://127.0.0.1:5000/modify/'+ str(data.id))
    print("test_edit_delete : ",r.status_code)

if __name__ == "__main__":
    test_home()
    test_edit()
    test_edit_post()
    test_edit_delete()