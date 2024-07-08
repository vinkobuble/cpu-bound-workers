import os

from aio_pika import Message
from fastapi import APIRouter

from rmq_setup.pika_setup import connect_exchange
from .schema import MultiplyMatricesRequestBody
from .worker_contract import MultiplyMatricesWorkerRequest

matrix_multiplication_router = APIRouter()


@matrix_multiplication_router.post("/submit-job/")
async def matrix_multiplication_submit_job(
    body: MultiplyMatricesRequestBody,
):
    worker_request = MultiplyMatricesWorkerRequest.model_validate(
        body.model_dump()
    )
    exchange_connection = await connect_exchange(
        exchange_name=os.environ['MATRIX_MULTIPLICATION_EXCHANGE'],
    )
    await exchange_connection.publish(
        Message(
            worker_request.model_dump_json().encode(),
            content_type='application/json',
        ),
        routing_key=os.environ['MATRIX_MULTIPLICATION_WORKER_ROUTING_KEY'],
    )
    return {"message": "scheduled"}
