from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = "users"
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="guest")
    last_login = Column(DateTime)


class RefreshToken(BareBaseModel):
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    refresh_token = Column(String, nullable=False)
    user = relationship("User")
