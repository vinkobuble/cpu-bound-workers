from fastapi import FastAPI

from health.api import health_router

app = FastAPI()

app.include_router(
    prefix="/health",
    router=health_router,
)
