import logging

from fastapi import Depends

from app.api.repository import project_repository
from app.helpers.paging import PaginationParams
from app.schemas.sche_project import CreateProject, UpdateProject


async def get_list_project(params: PaginationParams = Depends()):
    logging.info("===> get list project service <===")
    project = await project_repository.get_project(params)
    return {"data": project}


async def create_project(data: CreateProject):
    logging.info("===> create project service <===")
    project = await project_repository.create_project(data)
    return {"data": project}


async def update_project(project_id: int, data: UpdateProject):
    logging.info("===> update project service <===")
    project = await project_repository.update_project(project_id, data)
    return {"data": project}


async def get_project_detail(project_id: int):
    logging.info("===> get project detail service <===")
    project = await project_repository.get_project_detail(project_id)
    return {"data": project}
