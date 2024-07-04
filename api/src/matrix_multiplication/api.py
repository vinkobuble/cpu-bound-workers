import os

from fastapi import APIRouter

from rmq_setup.pika_setup import channel
from .schema import MultiplyMatricesRequestBody


matrix_multiplication_router = APIRouter()


@matrix_multiplication_router.post("/submit-job/")
def matrix_multiplication_submit_job(
    body: MultiplyMatricesRequestBody,
):
    channel.basic_publish(
        exchange=os.environ['MATRIX_MULTIPLICATION_EXCHANGE'],
        routing_key=os.environ['MATRIX_MULTIPLICATION_WORKER_ROUTING_KEY'],
        body=body.model_dump_json().encode()
    )
    return {"message": "scheduled"}
