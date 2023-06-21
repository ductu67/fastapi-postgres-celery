import logging

from app.api.repository import notification_repository
from app.schemas.sche_noti import RegisterFCMDevice


async def get_notification_by_id(user_id: int):
    logging.info("===> get notification service <===")
    notification = await notification_repository.get_notification_by_id(user_id)
    return notification


async def register_fcm_device_serv(data: RegisterFCMDevice):
    logging.info("===> register fcm device <===")
    response = await notification_repository.register_fcm_device_repo(data)
    return response
