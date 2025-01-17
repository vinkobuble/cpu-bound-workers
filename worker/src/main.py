"""Basic message consumer example"""
import functools
import logging
import os

import pika

from handler import on_message

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def main():
    """
    Connect to RabbitMQ and configure message consumer handler function.
    """
    credentials = pika.PlainCredentials(os.environ['RABBITMQ_USER'], os.environ['RABBITMQ_PASSWORD'])
    parameters = pika.ConnectionParameters(os.environ['RABBITMQ_HOST'], credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    on_message_callback = functools.partial(on_message)
    channel.basic_consume(os.environ['MATRIX_MULTIPLICATION_WORKER_QUEUE'], on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        # TODO: Graceful shutdown of the server.
        channel.stop_consuming()

    connection.close()


if __name__ == '__main__':
    main()
