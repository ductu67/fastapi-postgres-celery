import logging
from datetime import datetime

from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException
from fastapi_sqlalchemy import db
from starlette import status

from app.helpers.paging import PaginationParams, paginate
from app.models import Project
from app.schemas.sche_project import CreateProject, UpdateProject


async def get_project(params: PaginationParams = Depends()):
    try:
        logging.info("===> get list project repository <===")
        _query = db.session.query(Project)
        users = paginate(model=Project, query=_query, params=params)
        return users
    except ClientError as e:
        logging.error("===> Error project_repository.get_list_project <===")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


async def create_project(data: CreateProject):
    try:
        logging.info("===> create project repository <===")
        current_time = datetime.now()
        new_project = Project(project_name=data.project_name, created_at=current_time)
        db.session.add(new_project)
        db.session.commit()
        return new_project
    except ClientError as e:
        logging.error("===> Error project_repository.create_project <===")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


async def update_project(project_id: int, data: UpdateProject):
    try:
        logging.info("===> update project repository <===")
        current_time = datetime.now()
        current_project = db.session.query(Project).get(project_id)
        if current_project is None:
            raise Exception("Project not exist")
        current_project.project_name = (
            current_project.project_name
            if data.project_name is None
            else data.project_name
        )
        current_project.updated_at = current_time
        db.session.commit()
        return data
    except ClientError as e:
        logging.error("===> Error project_repository.update_project <===")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


async def get_project_detail(project_id: int):
    try:
        logging.info("===> get detail project repository <===")
        project = db.session.query(Project).get(project_id)
        if project is None:
            raise Exception("Project not exist")
        return project
    except ClientError as e:
        logging.error("===> Error project_repository.get_project_detail <===")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )
