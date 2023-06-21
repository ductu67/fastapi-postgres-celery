# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.model_notification import *  # noqa
from app.models.model_project import Project  # noqa
from app.models.model_user import User  # noqa
