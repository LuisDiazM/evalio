from pymongo import MongoClient
import os 

class Mongo:
    def __init__(self):
        conn_string = os.getenv("MONGO_URL","")
        client = MongoClient(conn_string)
        self.db = client["manager"]
