from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/")
async def health():
    return {"message": "All systems operating"}
