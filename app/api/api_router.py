from fastapi import APIRouter

from app.api.controller import (
    auth_controller,
    healthcheck_controller,
    project_controller, notification_controller,
)
from config.route import Route

router = APIRouter()

router.include_router(
    healthcheck_controller.router,
    prefix=Route.V1.prefix_api,
    tags=["Health-check"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    auth_controller.router,
    prefix=Route.V1.prefix_api,
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    project_controller.router,
    prefix=Route.V1.prefix_api,
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)
router.include_router(
    notification_controller.router,
    prefix=Route.V1.prefix_api,
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)