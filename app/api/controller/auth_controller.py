import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter

from app.api.service import auth_service
from app.schemas.sche_user import Login, Register
from config.route import Route
from exception import handle_exception

router = APIRouter()


@router.post(Route.V1.LOGIN)
async def login(user: Login):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function login <<<===")
    try:
        response = await auth_service.login(user=user)
        return response
    except ClientError or Exception as e:
        logging.error("===>>> Error auth_controller.login <<<===")
        logging.error(e)
        handle_exception.login_exception(e, user)


@router.post(Route.V1.REGISTER)
async def register(user_create: Register):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        return await auth_service.register(user_create=user_create)
    except ClientError or Exception as e:
        logging.error("===>>> Error register <<<===")
        logging.error(e)
        handle_exception.sign_up_exception(e, user_create)
