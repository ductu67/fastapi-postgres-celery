import logging
from datetime import datetime
from typing import Optional

import jwt
from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.helpers.exception_handler import CustomException
from app.models import User
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_user import (
    Login,
    Register,
    UserCreateRequest,
    UserUpdateMeRequest,
    UserUpdateRequest,
)
from config.messages_constant import ErrorCode


async def login(user: Login):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function login <<<===")
    user = UserService().authenticate(email=user.username_id, password=user.password)
    if not user:
        raise CustomException(http_code=400, code=ErrorCode.MSG_INVALID_EMAIL_PASSWORD["code"],
                              message=ErrorCode.MSG_INVALID_EMAIL_PASSWORD["message"])
    elif not user.is_active:
        raise CustomException(http_code=404, code=ErrorCode.MSG_ACTIVE_USER["code"],
                              message=ErrorCode.MSG_ACTIVE_USER["message"])

    user.last_login = datetime.now()
    db.session.commit()
    return {"access_token": create_access_token(user_id=user.id)}


async def register(user_create: Register):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        exist_user = (
            db.session.query(User).filter(User.email == user_create.email).first()
        )
        if exist_user:
            raise CustomException(http_code=400, code=ErrorCode.MSG_SIGNUP_EMAIL_EXISTS["code"],
                                  message=ErrorCode.MSG_SIGNUP_EMAIL_EXISTS["message"])
        UserService().register_user(user_create)
        return {
            "full_name": user_create.full_name,
            "email": user_create.email,
            "role": user_create.role,
        }
    except ClientError or Exception as e:  # ParamValidationError as e:
        logging.error("===>>> Error auth_service.register <<<===")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=e.response
        )


class UserService(object):
    __instance = None

    reusable_oauth2 = HTTPBearer(scheme_name="Authorization")

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials,
                settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM],
            )
            token_data = TokenPayload(**payload)
        except (jwt.PyJWTError, ValidationError):
            raise CustomException(http_code=400, code=ErrorCode.MSG_VALIDATE_CREDENTIAL["code"],
                                  message=ErrorCode.MSG_VALIDATE_CREDENTIAL["message"])
        user = db.session.query(User).get(token_data.user_id)
        if not user:
            raise CustomException(http_code=404, code=ErrorCode.MSG_USER_NOT_FOUND["code"],
                                  message=ErrorCode.MSG_USER_NOT_FOUND["message"])
        return user

    @staticmethod
    def register_user(data: Register):
        register_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True,
        )
        db.session.add(register_user)
        db.session.commit()
        return register_user

    @staticmethod
    def create_user(data: UserCreateRequest):
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_me(data: UserUpdateMeRequest, current_user: User):
        current_user.full_name = (
            current_user.full_name if data.full_name is None else data.full_name
        )
        current_user.email = current_user.email if data.email is None else data.email
        current_user.hashed_password = (
            current_user.hashed_password
            if data.password is None
            else get_password_hash(data.password)
        )
        db.session.commit()
        return current_user

    @staticmethod
    def update(user: User, data: UserUpdateRequest):
        user.full_name = user.full_name if data.full_name is None else data.full_name
        user.email = user.email if data.email is None else data.email
        user.hashed_password = (
            user.hashed_password
            if data.password is None
            else get_password_hash(data.password)
        )
        user.is_active = user.is_active if data.is_active is None else data.is_active
        user.role = user.role if data.role is None else data.role.value
        db.session.commit()
        return user
