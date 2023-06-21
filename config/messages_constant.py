class ErrorCode:
    MSG_LOGIN_INCORRECT = {
        # Incorrect username or password
        "code": 1,
        "message": "LOGIN FAIL",
    }
    MSG_LOGIN_USERNAME_EMPTY = {
        # Username cannot be empty
        "code": 2,
        "message": "USERNAME_EMPTY",
    }
    MSG_LOGIN_PASSWORD_EMPTY = {
        # Password cannot be empty
        "code": 3,
        "message": "PASSWORD_EMPTY",
    }
    MSG_SIGNUP_EMAIL = {
        # Username should be an email
        "code": 4,
        "message": "!!!",
    }
    MSG_SIGNUP_EMAIL_EXISTS = {
        # An account with the given email already exists
        "code": 5,
        "message": "Email already exists",
    }
    MSG_SIGNUP_USER_LENGTH = {
        # Invalid length for username. Valid min length: 1
        "code": 6,
        "message": "!!!",
    }
    MSG_SIGNUP_PASSWORD_LENGTH = {
        # Invalid length for username. Valid min length: 1
        "code": 6,
        "message": "!!!",
    }
    MSG_INVALID_EMAIL_PASSWORD = {
        "code": 7,
        "message": "Incorrect email or password",
    }
    MSG_ACTIVE_USER = {
        "code": 8,
        "message": "Inactive user",
    }
    MSG_USER_PERMISSION = {
        "code": 9,
        "message": "The user doesn't have enough privileges",
    }
    MSG_VALIDATE_CREDENTIAL = {
        "code": 10,
        "message": "Could not validate credentials",
    }
    MSG_USER_NOT_FOUND = {
        "code": 10,
        "message": "Could not validate credentials",
    }


class OthersException:
    MESSAGES_ERROR_SIGN_UP = "SIGN_UP ERROR"
