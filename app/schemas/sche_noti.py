from pydantic import BaseModel, EmailStr


class RegisterFCMDevice(BaseModel):
    user_id: int
    registration_id: str
    name: str = ""
    device_id: str = ""
    type: str = ""
    is_active: bool


class SendNotiTest(BaseModel):
    title: str
    message: str
    registration_ids: list


class EmailSchema(BaseModel):
    """Define the Email Schema."""
    recipients: list[EmailStr]
    subject: str
    body: str


class EmailTemplateSchema(BaseModel):
    """Define the Email Schema."""
    recipients: list[EmailStr]
    subject: str
    body: str
    template_name: str
