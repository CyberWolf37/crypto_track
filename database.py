from  dotenv import load_dotenv
import sqlite3
import os

class Crypto() :
    def __init__(self, name, price, how_many) :
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
        self.connection.execute("CREATE TABLE IF NOT EXISTS crypto_track\
            (\
                id INTEGER NOT NULL UNIQUE,\
                crypto_name VARCHAR(20) NOT NULL,\
                crypto_price FLOAT NOT NULL,\
                crypto_many FLOAT NOT NULL,\
                PRIMARY KEY(\"id\" AUTOINCREMENT)\
            )")
        self.connection.commit()

    def get_all_crypto(self, name) -> List[Crypto] :
        crypto_list = self.connection.execute("SELECT * FROM crypto_track")
        crypto_list = crypto_list.fetchall()
        crypto_list_obj = []
        for i in crypto_list :
            print(i)
            #crypto_list_obj.append()