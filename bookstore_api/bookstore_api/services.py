from datetime import datetime
import logging
import os

from pymongo import MongoClient
import pika


logger = logging.getLogger('book services')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

""" Enstablish a connection to mongo at the specified url and port """
def create_mongo_connection():
    client = MongoClient(os.getenv("MONGO_URL"), int(os.getenv("MONGO_PORT")))
    mongodb_connection = client.mongo_bookstore
    return mongodb_connection


""" Enstablish a connection to RabbitMQ """
def create_rabbitmq_connection():
    logger.info("# Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=os.getenv("RABBIT_MQ_OOO_BOOKS_QUEUE"))
    return channel


""" Publish a message to the queue """
def publish_notification(channel, routing_key, body):
    logger.info("# Publishing...")
    channel.basic_publish(exchange='',
                          routing_key=routing_key,
                          body=body)

    logger.info("# Sent notification for %s", body)


# def save_notification_on_mongo(ch, method, properties, body):
def save_notification_on_mongo(message, collection):
    # Process the message and persist in MongoDB
    notification_data = {
        # 'message': body.decode(),
        'message': message,
        'timestamp': datetime.now()
    }
    collection.insert_one(notification_data)