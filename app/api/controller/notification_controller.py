import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse

from app.api.service import notification_service
from app.celery_app import *
from app.helpers.login_manager import login_required
from app.helpers.send_mail import EmailTemplate
from app.schemas.sche_noti import RegisterFCMDevice, SendNotiTest, EmailSchema
from config.route import Route

router = APIRouter()


@router.get(Route.V1.GET_NOTIFICATION_BY_ID)
async def get_notification_by_id(user_id: int):
    logging.info("===>>> notification_controller.py <<<===")
    logging.info("===>>> function get_notification_by_id <<<===")
    try:
        response = await notification_service.get_notification_by_id(user_id)
        return response
    except ClientError or Exception as e:
        logging.error("===>>> Error notification_controller.get_notification <<<===")
        logging.error(e)


@router.post(Route.V1.REGISTER_FCM_DEVICE, dependencies=[Depends(login_required)])
async def register_fcm_device(data: RegisterFCMDevice):
    logging.info("===>>> notification_controller.py <<<===")
    logging.info("===>>> function register_fcm_device <<<===")
    try:
        response = await notification_service.register_fcm_device_serv(data)
        return response
    except ClientError or Exception as e:
        logging.error("===>>> Error notification_controller.register_fcm_device <<<===")
        logging.error(e)


@router.post(Route.V1.TEST_FUNCTION)
async def test_notification(data: SendNotiTest):
    logging.info("===>>> notification_controller.py <<<===")
    logging.info("===>>> function test_notification <<<===")
    try:
        # send_push_notification.delay("dasfasdf")
        send_notification_for_test.delay(data.title, data.message, data.registration_ids)
        return []
    except ClientError or Exception as e:
        logging.error("===>>> Error notification_controller.test_notification <<<===")
        logging.error(e)


@router.post(Route.V1.EMAIL)
async def simple_send(email: EmailSchema) -> JSONResponse:
    mail_template = EmailTemplate()
    await mail_template.send_mail_to_user(subject=email.subject, template_name="verification", user_name="TuND",
                                          email=email.recipients)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
