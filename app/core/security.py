import logging
from datetime import datetime, timedelta

import jwt
from botocore.exceptions import ClientError
from passlib.context import CryptContext

from app.core.config import settings
from app.helpers.exception_handler import CustomException
from app.schemas.sche_user import TokenData
from config.messages_constant import ErrorCode

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_SECONDS) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.REFRESH_KEY, algorithms=settings.SECURITY_ALGORITHM)
        user_id = payload.get("user_id")
        user_email = payload.get("email")
        if user_id is None:
            raise CustomException(http_code=400, code=ErrorCode.MSG_VALIDATE_CREDENTIAL["code"],
                                  message=ErrorCode.MSG_VALIDATE_CREDENTIAL["message"])
        token_data = TokenData(user_id=user_id, email=user_email)
    except ClientError or Exception as e:
        logging.error(e)
        raise CustomException(http_code=400, code=ErrorCode.MSG_VALIDATE_CREDENTIAL["code"],
                              message=ErrorCode.MSG_VALIDATE_CREDENTIAL["message"])
    return token_data


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
