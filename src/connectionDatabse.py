from pymongo import MongoClient

class Connection:
# This class is use to connect the 
# mongo database and return the instace 
# connection

    @staticmethod
    def connectionDatabase():
        client = MongoClient('mongodb://localhost:27017/')  
        database = client['teste']
        return database