import os
from http import HTTPStatus
from typing import Final

import aiohttp
from fastapi import APIRouter

desired_worker_scale_router = APIRouter()

AVERAGE_LENGTH_OF_JOB_IN_SEC: Final = 20
MINIMUM_NUMBER_OF_WORKER_INSTANCES: Final = 2
MAXIMUM_NUMBER_OF_WORKER_INSTANCES: Final = 200


@desired_worker_scale_router.get("/")
async def desired_worker_scale():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"http://"
                f"{os.environ["RABBITMQ_USER"]}:{os.environ["RABBITMQ_PASSWORD"]}"
                f"@{os.environ["RABBITMQ_HOST"]}"
                f":{os.environ["RABBITMQ_MANAGEMENT_PORT"]}/api/queues/%2F/"
                f"{os.environ['MATRIX_MULTIPLICATION_WORKER_QUEUE']}"
        ) as response:
            if response.status != HTTPStatus.OK:
                raise RuntimeError(f"Unable to get {os.environ['MATRIX_MULTIPLICATION_WORKER_QUEUE']} queue stats!")
            response_data = await response.json()
            queue_publish_rate = response_data["message_stats"]["publish_details"]["rate"]
            message_count = response_data["messages"]
            desired_scale_by_publish_rate = max(
                MINIMUM_NUMBER_OF_WORKER_INSTANCES,
                min(
                    AVERAGE_LENGTH_OF_JOB_IN_SEC * queue_publish_rate
                    if queue_publish_rate != 0.0 else MINIMUM_NUMBER_OF_WORKER_INSTANCES,
                    MAXIMUM_NUMBER_OF_WORKER_INSTANCES
                )
            )
            desired_scale_by_messages_in_queue = max(
                MINIMUM_NUMBER_OF_WORKER_INSTANCES,
                min(
                    message_count,
                    MAXIMUM_NUMBER_OF_WORKER_INSTANCES
                )
            )

    return {"desired-worker-scale": max(desired_scale_by_publish_rate, desired_scale_by_messages_in_queue)}
