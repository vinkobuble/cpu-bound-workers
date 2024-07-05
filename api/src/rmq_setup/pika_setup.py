import os

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ['RABBITMQ_HOST']
    )
)
channel = connection.channel()
