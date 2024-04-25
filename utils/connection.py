from pymongo import MongoClient


def get_connection():
    url_connection = 'mongodb+srv://vinceparra77:HeyLtSJ4EAfDWeAD@cluster0.6g8b8yi.mongodb.net/'
    client = MongoClient(url_connection)
    return client['Meteorite']
