from pymongo import MongoClient
import os


class MongoDB:
    client: MongoClient

    def __init__(self):
        url = os.getenv("MONGO_URL")
        if not url:
            raise ValueError("MONGO_URL environment variable is not set.")
        self.client = MongoClient(url)
