import os

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ['RABBIT_MQ_HOST']
    )
)
channel = connection.channel()
