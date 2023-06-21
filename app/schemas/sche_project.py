from pydantic import BaseModel


class CreateProject(BaseModel):
    project_name: str


class UpdateProject(BaseModel):
    project_name: str
