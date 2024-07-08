from fastapi import FastAPI

from health.api import health_router
from desired_worker_scale.api import desired_worker_scale_router

app = FastAPI()

app.include_router(
    prefix="/health",
    router=health_router,
)
app.include_router(
    prefix="/desired-worker-scale",
    router=desired_worker_scale_router,
)

