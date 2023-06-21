import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from app.api.service import project_service
from app.helpers.login_manager import login_required
from app.helpers.paging import PaginationParams
from app.schemas.sche_project import CreateProject, UpdateProject
from config.route import Route

router = APIRouter()


@router.get(Route.V1.GET_LIST_PROJECT, dependencies=[Depends(login_required)])
async def get_list_project(params: PaginationParams = Depends()):
    logging.info("===> function get_list_project <===")
    try:
        return await project_service.get_list_project(params)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.get_list_project <<<===")
        logging.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


@router.post(Route.V1.CREATE_PROJECT, dependencies=[Depends(login_required)])
async def create_project(project_name: str = Form(...)):
    logging.info("===> function create_project <===")
    try:
        request_data = CreateProject(
            **{
                "project_name": project_name,
            }
        )
        return await project_service.create_project(request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.create_project <<<===")
        logging.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


@router.put(Route.V1.UPDATE_PROJECT, dependencies=[Depends(login_required)])
async def update_project(project_id: int, project_name: str = Form(...)):
    logging.info("===> function update_project <===")
    try:
        request_data = UpdateProject(
            **{
                "project_name": project_name,
            }
        )
        return await project_service.update_project(project_id, request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.create_project <<<===")
        logging.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )


@router.get(Route.V1.GET_PROJECT_DETAIL, dependencies=[Depends(login_required)])
async def get_project_detail(project_id: int):
    logging.info("===> function get_list_project <===")
    try:
        return await project_service.get_project_detail(project_id)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.get_project_detail <<<===")
        logging.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response
        )
