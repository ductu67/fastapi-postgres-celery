from sqlalchemy import Column, String, Boolean, ForeignKey, Integer

from app.models.model_base import BareBaseModel


class Notification(BareBaseModel):
    __tablename__ = "notifications"
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"))
    url_path = Column(String, nullable=True)
    title = Column(String, nullable=True)
    message = Column(String, nullable=True)
    status = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)


class FCMDevice(BareBaseModel):
    __tablename__ = "fcm_device"
    user_id = Column(Integer, ForeignKey("users.id"))
    registration_id = Column(String)
    name = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    type = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
