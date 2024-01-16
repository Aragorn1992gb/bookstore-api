from pymongo import MongoClient
import os

import logging

logger = logging.getLogger('book services')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# create connection to mongo at the specified url and port
def create_mongo_connection():
    client = MongoClient(os.getenv("MONGO_URL"), int(os.getenv("MONGO_PORT")))
    db = client.mongo_bookstore
    return db