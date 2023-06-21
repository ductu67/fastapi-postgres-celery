from celery import Celery
from celery.schedules import crontab
from pyfcm import FCMNotification

from app.core.config import settings
from app.db.base import SessionLocal
from app.models import Notification, FCMDevice

celery = Celery(__name__,
                broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)

celery.autodiscover_tasks()

# celery.conf.beat_schedule = {
#     'remind vehicle registration': {
#         'task': 'app.celery_app.remind_vehicle_registration',
#         'schedule': crontab(minute=0, hour='9'),
#     },
#
# }

push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)


# https://pypi.org/project/pyfcm/
# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

@celery.task()
def send_notification_for_test(title, message, registration_ids):
    message_title = title
    message_body = message
    if registration_ids:
        push_service.notify_multiple_devices(registration_ids=registration_ids,
                                             message_title=message_title,
                                             message_body=message_body)
    return


@celery.task()
def send_notification_for_user(notification_id):
    session = SessionLocal()
    notification = session.query(Notification).filter_by(id=notification_id).first()
    devices = session.query(FCMDevice).filter_by(user_id=notification.receiver_id)
    message_title = notification.title
    message_body = notification.message
    registration_ids = [obj.registration_id for obj in devices.distinct()]
    if registration_ids:
        push_service.notify_multiple_devices(registration_ids=registration_ids,
                                             message_title=message_title,
                                             message_body=message_body)
    return
