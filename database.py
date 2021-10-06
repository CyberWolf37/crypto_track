from  dotenv import load_dotenv
from typing import List
import sqlite3
import os

class Crypto() :
    def __init__(self ,name, price, how_many, id = None) :
        self.id = id
        self.name = name
        self.price = price
        self.how_many = how_many

class Database() :

    def __init__(self) :
        # loading env
        load_dotenv("./app.env")

        # prepare connection
        path = os.environ.get("PATH_SQLITE_DB")
        conn = sqlite3.connect(path)
        self.connection = conn
        
        # Init the table if does not exist
        self.initiation()

    def initiation(self) :
        try :
            self.connection.execute("CREATE TABLE IF NOT EXISTS crypto_track\
                (\
                    id INTEGER NOT NULL UNIQUE,\
                    crypto_name VARCHAR(20) NOT NULL,\
                    crypto_price FLOAT NOT NULL,\
                    crypto_many FLOAT NOT NULL,\
                    PRIMARY KEY(\"id\" AUTOINCREMENT)\
                )")
            self.connection.commit()
        except :
            print("oops the init table of sqlite3 has failed")

    def get_all_crypto(self) -> List[Crypto] :
        try :
            crypto_list = self.connection.execute("SELECT * FROM crypto_track")
            crypto_list = crypto_list.fetchall()
            crypto_list_obj = []
            for i in crypto_list :

                cryo = Crypto(id=i[0],name=i[1],price=i[2],how_many=i[3])
                crypto_list_obj.append(cryo)

            return crypto_list_obj
        except :
            print("oops an error occurred in function get_all_crypto")

    def insert_crypto(self, crypto: Crypto) :
        try:
            query = """INSERT INTO crypto_track(crypto_name, crypto_price, crypto_many) VALUES(?,?,?)"""
            params = (crypto.name,crypto.price,crypto.how_many)
            self.connection.execute(query,params)
            self.connection.commit()
        except :
            print("oops an error occured in function insert_crypto")

    def remove_crypto(self, id) :
        try:
            self.connection.execute("DELETE FROM crypto_track WHERE id='%s'" %id)
            self.connection.commit()
        except :
            print( "oops the remove object has failed")