from sqlalchemy import Column, DateTime, String

from app.models.model_base import BareBaseModel


class Project(BareBaseModel):
    project_name = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
