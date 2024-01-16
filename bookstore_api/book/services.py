import logging
import os
from pymongo import MongoClient

logger = logging.getLogger('book services')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

""" Create connection to mongo at the specified url and port """
def create_mongo_connection():
    client = MongoClient(os.getenv("MONGO_URL"), int(os.getenv("MONGO_PORT")))
    mongodb_connection = client.mongo_bookstore
    return mongodb_connection
