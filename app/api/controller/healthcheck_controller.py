from fastapi import APIRouter

from config.route import Route

router = APIRouter()


@router.get(Route.V1.HEALTH_CHECK)
async def get_health_check():
    return {"message": "Health check success"}
