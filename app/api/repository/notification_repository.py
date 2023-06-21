import logging

from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi_sqlalchemy import db
from starlette import status

from app.models import FCMDevice
from app.models.model_notification import Notification
from app.schemas.sche_base import DataResponse
from app.schemas.sche_noti import RegisterFCMDevice


async def get_notification_by_id(user_id: int):
    try:
        logging.info("===> get notification repository <===")
        list_notification_by_id = db.session.query(Notification).filter_by(receiver_id=user_id).all()
        return DataResponse().success_response(list_notification_by_id)
    except ClientError as e:
        logging.error("===> Error notification_repository.get_notification_by_id <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def register_fcm_device_repo(data: RegisterFCMDevice):
    try:
        logging.info("===> register fcm device repository <===")
        new_device = FCMDevice(
            user_id=data.user_id,
            registration_id=data.registration_id,
            name=data.name,
            device_id=data.device_id,
            type=data.type,
            is_active=data.is_active,
        )
        db.session.add(new_device)
        db.session.commit()
        return DataResponse().success_response(new_device)
    except ClientError as e:
        logging.error("===> Error notification_repository.register_fcm_device_repo <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
