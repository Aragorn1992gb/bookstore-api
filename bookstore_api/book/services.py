from pymongo import MongoClient
import os

import logging

logger = logging.getLogger('book services')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

def create_mongo_connection():
    client = MongoClient(os.getenv("MONGO_ROOT"), int(os.getenv("MONGO_PORT")))
    db = client.mongo_bookstore
    return db