import os

import aio_pika


async def rmq_connection() -> aio_pika.abc.AbstractRobustConnection:
    connection = await aio_pika.connect_robust(
        host=os.environ['RABBITMQ_HOST']
    )
    return connection


async def connect_exchange(exchange_name: str) -> aio_pika.abc.AbstractExchange:
    connection = await rmq_connection()
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    return await channel.declare_exchange(
        exchange_name,
        durable=True,
        passive=True
    )
