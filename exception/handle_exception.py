from fastapi import HTTPException

from config import messages_constant
from config.messages_constant import ErrorCode


def login_exception(e, user):
    if e.response["Error"]["Code"] == "NotAuthorizedException":
        raise HTTPException(
            status_code=e.response["ResponseMetadata"]["HTTPStatusCode"],
            detail=ErrorCode.MSG_LOGIN_INCORRECT,
        )
    elif e.response["Error"]["Code"] == "InvalidParameterException":
        if not user.username_id:
            raise HTTPException(
                status_code=e.response["ResponseMetadata"]["HTTPStatusCode"],
                detail=ErrorCode.MSG_LOGIN_USERNAME_EMPTY,
            )

        if not user.password:
            raise HTTPException(
                status_code=e.response["ResponseMetadata"]["HTTPStatusCode"],
                detail=ErrorCode.MSG_LOGIN_PASSWORD_EMPTY,
            )
    else:
        raise HTTPException(status_code=400, detail=str(e))


def sign_up_exception(e, user_create=None):
    if type(e).__name__ == "InvalidParameterException":
        raise HTTPException(
            status_code=400, detail=ErrorCode.MSG_SIGNUP_EMAIL.get("message")
        )
    elif type(e).__name__ == "UsernameExistsException":
        raise HTTPException(
            status_code=400, detail=ErrorCode.MSG_SIGNUP_EMAIL_EXISTS.get("message")
        )
    elif type(e).__name__ == "ParamValidationError":
        if str(e)[-1] == "1":
            raise HTTPException(
                status_code=400, detail=ErrorCode.MSG_SIGNUP_USER_LENGTH.get("message")
            )
        elif str(e)[-1] == "6":
            raise HTTPException(
                status_code=400,
                detail=ErrorCode.MSG_SIGNUP_PASSWORD_LENGTH.get("message"),
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=messages_constant.OthersException.MESSAGES_ERROR_SIGN_UP,
        )
