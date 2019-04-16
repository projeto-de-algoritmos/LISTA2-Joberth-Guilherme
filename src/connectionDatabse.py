from pymongo import MongoClient

class Connection:

    @staticmethod
    def connectionDatabase():
        client = MongoClient('mongodb://localhost:27017/')  
        database = client['matriculaweb']
        return database
