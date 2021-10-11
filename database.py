from  dotenv import load_dotenv
import traceback
import sys
from itertools import chain
from typing import List
import sqlite3
import os
from datetime import datetime

class Crypto_label() :
    def __init__(self ,id ,symbol ,name) :
        self.id = id
        self.symbol = symbol
        self.name = name

class Crypto() :
    def __init__(self ,crypto_id ,price, how_many, when = datetime.now(), id = None,last_price_quote=None) :
        self.id = id
        self.crypto_id = crypto_id
        self.price = price
        self.how_many = how_many
        self.when = when
        self.value = float(price) * float(how_many)

class Crypto_full() :
    def __init__(self ,id ,id_crypto ,symbol ,crypto_name ,price ,how_many, when, last_price_quote=None) :
        self.id = id
        self.id_crypto = id_crypto
        self.symbol = symbol
        self.name = crypto_name
        self.price = price
        self.how_many = how_many
        self.when = when
        self.last_price_quote = last_price_quote
        self.value = price * how_many

class Crypto_quote() :
    def __init__(self ,id, price, when) :
        self.id = id
        self.price = price
        self.when = when

class Database() :

    def __init__(self) :
        # prepare connection
        path = os.environ.get("PATH_SQLITE_DB")
        conn = sqlite3.connect(path,check_same_thread=False)
        self.connection = conn
        
        # Init the table if does not exist
        self.initiation()

    def initiation(self) :
        try :
            self.connection.execute("CREATE TABLE IF NOT EXISTS crypto\
                (\
                    id INTEGER NOT NULL UNIQUE,\
                    crypto_symbol VARCHAR(20) NOT NULL,\
                    crypto_label VARCHAR(50) NOT NULL,\
                    PRIMARY KEY(\"id\" AUTOINCREMENT)\
                )")
            self.connection.commit()
            self.connection.execute("CREATE TABLE IF NOT EXISTS crypto_track\
                (\
                    id INTEGER NOT NULL UNIQUE,\
                    crypto_id INTEGER NOT NULL,\
                    crypto_price FLOAT NOT NULL,\
                    crypto_many FLOAT NOT NULL,\
                    crypto_when DATETIME NOT NULL,\
                    PRIMARY KEY(\"id\" AUTOINCREMENT)\
                    FOREIGN KEY(crypto_id) REFERENCES crypto(id)\
                )")
            self.connection.commit()
            self.connection.execute("CREATE TABLE IF NOT EXISTS crypto_quote\
                (\
                    id INTEGER NOT NULL UNIQUE,\
                    crypto_id INTEGER NOT NULL,\
                    crypto_price FLOAT NOT NULL,\
                    crypto_when DATETIME NOT NULL,\
                    PRIMARY KEY(\"id\" AUTOINCREMENT)\
                    FOREIGN KEY(crypto_id) REFERENCES crypto(id)\
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

                cryo = Crypto(id=i[0],crypto_id=i[1],price=i[2],how_many=i[3],when=i[4])
                crypto_list_obj.append(cryo)

            return crypto_list_obj
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_last_crypto(self) -> Crypto :
        try :
            crypto_list = self.connection.execute("SELECT * FROM crypto_track ORDER BY crypto_id DESC LIMIT 1")
            i = crypto_list.fetchone()
            cryo = Crypto(id=i[0],crypto_id=i[1],price=i[2],how_many=i[3],when=i[4])

            return cryo

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_all_crypto_labels(self) -> List[Crypto_label] :
        try :
            crypto_list = self.connection.execute("SELECT * FROM crypto")
            crypto_list = crypto_list.fetchall()
            crypto_list_obj = []
            for i in crypto_list :

                cryo = Crypto_label(id=i[0],symbol=i[1],name=i[1])
                crypto_list_obj.append(cryo)

            return crypto_list_obj
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_all_crypto_full(self) -> List[Crypto_full]:
        try :
            crypto_list = self.connection.execute(
                "SELECT crypto.id, crypto_track.id, crypto.crypto_symbol, crypto.crypto_label, crypto_track.crypto_price, crypto_track.crypto_many, crypto_track.crypto_when\
                 FROM crypto, crypto_track\
                 WHERE crypto.id = crypto_track.crypto_id")
            crypto_list = crypto_list.fetchall()
            crypto_list_obj = []
            for i in crypto_list :
                cryo = Crypto_full(id=i[0],id_crypto=i[1],symbol=i[2] ,crypto_name=i[3] ,price=i[4] ,how_many=i[5], when=i[6], last_price_quote=self.get_last_price_by_id(i[0]))
                crypto_list_obj.append(cryo)

            return crypto_list_obj
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_all_crypto_quote_by_name(self,name) -> List[Crypto_quote] :
        try :
            crypto_list = self.connection.execute("SELECT * FROM crypto_quote WHERE crypto_name='%s'" %name)
            crypto_list = crypto_list.fetchall()
            crypto_list_obj = []
            for i in crypto_list :
                cryo = Crypto_quote(name=i[1],price=i[2],when=datetime(i[3]))
                crypto_list_obj.append(cryo)

            return crypto_list_obj
        except :
            print("oops an error occurred in function get_all_crypto_by_name")

    def get_all_crypto_symbol(self) -> List[str] :
        try :
            crypto_list = self.connection.execute("SELECT crypto_symbol FROM crypto")
            crypto_list = crypto_list.fetchall()
            list_obj = []

            for i in crypto_list :
                list_obj = chain(list_obj,list(i))
            return list_obj
        except :
            print("oops an error occurred in function get_all_crypto_by_name")
    

    def get_all_crypto_symbol_label(self) :
        try :
            crypto_list = self.connection.execute("SELECT crypto_symbol, crypto_label  FROM crypto")
            crypto_list = crypto_list.fetchall()

            return crypto_list
        except :
            print("oops an error occurred in function get_all_crypto_by_name")
    
    def get_crypto_by_id(self,id) :
        try :
            crypto_list = self.connection.execute("SELECT *  FROM crypto_track WHERE id='%s'" %id)
            crypto = crypto_list.fetchone()

            cryo = Crypto(id=crypto[0],crypto_id=crypto[1],price=crypto[2],how_many=crypto[3],when=crypto[4])

            return cryo
        except :
            print("oops an error occurred in function get_all_crypto_by_name")

    def get_id_by_symbol(self,symbol) :
        try :
            crypto_list = self.connection.execute("SELECT id  FROM crypto WHERE crypto_symbol='%s'" %symbol)
            sym = crypto_list.fetchone()[0]

            return sym
        except :
            print("oops an error occurred in function get_all_crypto_by_name")

    def get_all_crypto_price_by_name(self,name) -> List[str] :
        try :
            crypto_list = self.connection.execute("SELECT crypto_price FROM crypto_quote WHERE crypto_name='%s'" %name)
            crypto_list = crypto_list.fetchall()

            return crypto_list
        except :
            print("oops an error occurred in function get_all_crypto_price_by_name")

    def insert_crypto(self, crypto: Crypto) :
        try:
            query = """INSERT INTO crypto_track(crypto_id, crypto_price, crypto_many, crypto_when) VALUES(?,?,?,?)"""
            params = (crypto.crypto_id,crypto.price,crypto.how_many,crypto.when)
            self.connection.execute(query,params)
            self.connection.commit()

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def insert_crypto_quote(self, crypto: Crypto_quote) :
        try:
            query = """INSERT INTO crypto_quote(crypto_id, crypto_price, crypto_when) VALUES(?,?,?)"""
            params = (crypto.id,crypto.price,crypto.when)
            self.connection.execute(query,params)
            self.connection.commit()

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def remove_crypto(self, id) :
        try:
            self.connection.execute("DELETE FROM crypto_track WHERE id='%s'" %id)
            self.connection.commit()
        except :
            print( "oops the remove object has failed")

    def modify_crypto(self, id, id_crypto, price, many) :
        try:
            query = """UPDATE crypto_track SET crypto_id = ?,crypto_price = ?, crypto_many = ? WHERE id=? """
            params = (id_crypto,price,many,id)
            self.connection.execute(query,params)
            self.connection.commit()

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_last_price_by_id(self, id) :
        try:
            query = "SELECT crypto_price FROM crypto_quote WHERE crypto_id=\'%s\' ORDER BY crypto_when DESC LIMIT 1" %id
            list = self.connection.execute(query)
            price = list.fetchone()[0]
            return price

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_all_price_by_id(self, id) -> List[str] :
        try:
            query = "SELECT crypto_price FROM crypto_quote WHERE crypto_id=\'%s\' ORDER BY crypto_when ASC" %id
            list = self.connection.execute(query)
            prices = list.fetchall()
            list_obj = []

            for price in prices :
                list_obj.append(price[0])

            return list_obj

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_all_date_by_id(self, id) -> List[str] :
        try:
            query = "SELECT crypto_when FROM crypto_quote WHERE crypto_id=\'%s\' ORDER BY crypto_when ASC" %id
            list = self.connection.execute(query)
            dates = list.fetchall()
            list_obj = []

            for date in dates :
                list_obj.append(date[0])

            return list_obj

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_last_date(self) :
        try:
            query = "SELECT crypto_when FROM crypto_quote ORDER BY crypto_when DESC LIMIT 1"
            list = self.connection.execute(query)
            date = list.fetchone()[0]

            return date

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))