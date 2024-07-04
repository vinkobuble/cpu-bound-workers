from fastapi import APIRouter

from .schema import MultiplyMatrices

matrix_multiplication_router = APIRouter()


@matrix_multiplication_router.post("submit-job/")
def matrix_multiplication_submit_job(
    body: MultiplyMatrices,
):
    # TODO: publishing to RabbitMQ
    return {"message": "scheduled"}
