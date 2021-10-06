from database import Crypto, Database


if __name__ == '__main__':
    db = Database()

    list = db.get_all_crypto()

    db.remove_crypto(5)
