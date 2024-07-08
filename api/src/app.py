from fastapi import FastAPI

from health.api import health_router
from matrix_multiplication.api import matrix_multiplication_router

app = FastAPI()

app.include_router(
    prefix="/health",
    router=health_router,
)
app.include_router(
    prefix="/matrix-multiplication",
    router=matrix_multiplication_router,
)
