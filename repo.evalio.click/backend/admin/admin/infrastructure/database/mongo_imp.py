from pymongo import MongoClient
import os

DATABASE_NAME = "manager"


class Mongo:
    def __init__(self):
        conn_string = os.getenv("MONGO_URL", "")
        if conn_string == "":
            raise ValueError("MONGO_URL environment variable is not set")
        client = MongoClient(conn_string)
        self.db = client[DATABASE_NAME]
